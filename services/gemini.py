from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.dependencies import get_db
from google import genai
from google.genai import types
from declarations.accidents import get_accident_count_tool
from routers.accidents import get_accidents_count
from config import system_instructions
from dotenv import load_dotenv
import os, logging
from typing import Any

load_dotenv()
logger = logging.getLogger(__name__)
router = APIRouter()

TOOL_REGISTRY = {
    "get_accidents_count": get_accidents_count
}


class ChatRequest(BaseModel):
    message: str

def _invoke_tool(tool_obj: Any, db: Session, args: dict):
    if callable(tool_obj):
        code = getattr(tool_obj, "__code__", None)
        if code and "db" in code.co_varnames:
            return tool_obj(db=db, **args)
        return tool_obj(**args)
    raise HTTPException(status_code=500, detail=f"Tool not callable: {type(tool_obj)}")

def handle_gemini_response(chat, response, db: Session):
    candidate = response.candidates[0]
    while candidate.content.parts and hasattr(candidate.content.parts[0], "function_call") and candidate.content.parts[0].function_call:
        fc = candidate.content.parts[0].function_call
        tool_name = fc.name
        tool = TOOL_REGISTRY.get(tool_name)
        if not tool:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
        args = fc.args or {}
        output = _invoke_tool(tool, db, args)
        response = chat.send_message(
            types.Content(parts=[types.Part(function_response=types.FunctionResponse(name=tool_name, response=output))])
        )
        candidate = response.candidates[0]
    for part in candidate.content.parts:
        if hasattr(part, "text") and part.text:
            return part.text
    return "No text response from Gemini."

@router.post("/chat")
def chat_with_gemini(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        api_key = os.getenv("LLM_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="LLM_API_KEY not set")
        client = genai.Client(api_key=api_key)
        config = types.GenerateContentConfig(tools=[get_accident_count_tool], system_instruction=system_instructions)
        response = client.models.generate_content(model="gemini-2.5-flash", contents=req.message, config=config)
        if not getattr(response, "function_calls", None):
            return {"response": response.text}
        fcall = response.function_calls[0]
        fn_name = fcall.name
        args = fcall.args or {}
        if fn_name not in TOOL_REGISTRY:
            raise HTTPException(status_code=500, detail=f"Unknown tool: {fn_name}")
        tool_fn = TOOL_REGISTRY[fn_name]
        output = _invoke_tool(tool_fn, db, args)
        func_resp_part = types.Part.from_function_response(name=fn_name, response=output)
        func_call_part = types.Part.from_function_call(fcall)
        user_content = types.Content(parts=[types.Part(text=req.message)])
        func_call_content = types.Content(parts=[func_call_part])
        func_resp_content = types.Content(parts=[func_resp_part])
        followup = client.models.generate_content(model="gemini-2.5-flash", contents=[user_content, func_call_content, func_resp_content], config=config)
        return {"response": followup.text}
    except Exception as e:
        logger.error(f"Gemini chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Gemini backend error: {str(e)}")
