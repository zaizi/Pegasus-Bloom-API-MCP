from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.dependencies import get_db
from google.genai import types, Client
from declarations.accidents import get_accident_count_tool
from routers.accidents import get_accidents_count
from config import system_instructions
from pydantic import BaseModel
from dotenv import load_dotenv
import os, logging
load_dotenv()
logger = logging.getLogger(__name__)
router = APIRouter()

tools = types.Tool(function_declarations=[get_accident_count_tool])

available_tools = {
    "get_accidents_count": get_accidents_count,
}


class ChatRequest(BaseModel):
    prompt: str

@router.post("/chat")
def chat_with_gemini(request: ChatRequest, db: Session = Depends(get_db)): 
    try:
        api_key = os.getenv("LLM_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="LLM_API_KEY not set")
        
        config = types.GenerateContentConfig(tools=[tools], system_instruction=system_instructions)
        with Client(api_key=api_key) as client:
            chat = client.chats.create(model="gemini-2.5-flash", config=config)
            response = chat.send_message(message = request.prompt)
            part = response.parts[0]

            #step 2 - Check if the model returned a function call
            if not part.function_call.name:

                # No function call, just a simple text response.
                return {"response": response.text}
            
            # step 3 - Execute the function call
            fc = part.function_call
            function_name = fc.name
            
            if function_name not in available_tools:
                raise HTTPException(status_code=500, detail=f"Model requested unknown function: {function_name}")
            
            # Get the actual Python function from our map
            function_to_call = available_tools[function_name]
            
            # Get the arguments from the model (convert from 'Struct' to 'dict')
            function_args = dict(fc.args)
            function_args['db'] = db
            # Call our local Python function with the arguments
            function_result = function_to_call(**function_args)
            
            #STEP 4: Send the function's result back to the model
            final_response = chat.send_message(
                message=types.Part.from_function_response(
                    name=function_name,
                    response=function_result  # Send the dictionary back
                )
            )
            
            # The model will now use this result to give a natural language answer as a result of the function. The response was a function, not text, originally.
            return {"response": final_response.text}

    except Exception as e:
        logger.error(f"Gemini chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Gemini backend error: {str(e)}")