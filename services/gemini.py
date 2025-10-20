from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.dependencies import get_db
from google import genai
from google.genai import types
from declarations.accidents import get_accident_count_tool
from config import system_instructions
from dotenv import load_dotenv
import os, logging
from typing import Any

load_dotenv()
logger = logging.getLogger(__name__)
router = APIRouter()

TOOL_REGISTRY = {"get_count_accidents": get_accident_count_tool}

class ChatRequest(BaseModel):
    message: str

def _invoke_tool(tool_obj: Any, db: Session, args: dict):
    if callable(tool_obj):
        return tool_obj(db=db, **args) if "db" in getattr(tool_obj, "__code__", {}).co_varnames else tool_obj(**args)

    for attr in ("func", "fn", "implementation", "run", "callable"):
        cand = getattr(tool_obj, attr, None)
        if callable(cand):
            return cand(db=db, **args) if "db" in getattr(cand, "__code__", {}).co_varnames else cand(**args)

    raise HTTPException(status_code=500, detail=f"Tool is not callable and no underlying function found: {type(tool_obj)}")

def handle_gemini_response(chat, response, db: Session):
    candidate = response.candidates[0]
    while candidate.content.parts and getattr(candidate.content.parts[0], "function_call", None):
        fc = candidate.content.parts[0].function_call
        tool_name = fc.name
        tool = TOOL_REGISTRY.get(tool_name)
        if not tool:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
        args = fc.args or {}
        output = _invoke_tool(tool, db, args)
        response = chat.send_message(
            types.Content(parts=[
                types.Part(function_response=types.FunctionResponse(name=tool_name, response=output))
            ])
        )
        candidate = response.candidates[0]

    if candidate.content.parts and hasattr(candidate.content.parts[0], "text"):
        return candidate.content.parts[0].text

    return "No text response from Gemini."

@router.post("/chat")
def chat_with_gemini(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        client = genai.Client(api_key=os.getenv("LLM_API_KEY"))
        config = types.GenerateContentConfig(
            tools=[get_accident_count_tool],
            system_instruction=system_instructions,
        )
        chat = client.models.generate_content(model="gemini-2.5-flash",contents=req, config=config)
        initial = chat.candidates[0]
        result = handle_gemini_response(chat, initial, db)
        return {"response": result}
    except Exception as e:
        logger.error(f"Gemini chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Gemini backend error")
