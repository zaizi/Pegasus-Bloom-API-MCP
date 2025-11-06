import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.dependencies import get_db
from declarations.aws_tool_declarations import tool_specifications
from config import aws_system_instructions
from pydantic import BaseModel
from dotenv import load_dotenv
import json, decimal, datetime
import logging

load_dotenv()
logger = logging.getLogger(__name__)
router = APIRouter()

#need to import the *actual* functions to call them
from routers.accidents import get_accidents_count
from routers.report_generation import generate_service_user_report

available_tools = {
    "get_accidents_count": get_accidents_count,
    "generate_service_user_report": generate_service_user_report,
}

def json_serialize(data):
    def default(o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        raise TypeError(f"Type not serializable: {type(o)}")
    
    return json.loads(json.dumps(data, default=default))


#Boto3 Client & Model Config
try:
    brt = boto3.client(service_name="bedrock-runtime", region_name="eu-west-2")
    model_id = "openai.gpt-oss-20b-1:0"
except Exception as e:
    logger.error(f"Failed to initialize Boto3 client: {e}")
    brt = None



class ChatRequest(BaseModel):
    prompt: str
    # can expand this to include a full message history
    # messages: list 



@router.post("/aws_chat/")
def chat_with_aws(request: ChatRequest, db: Session = Depends(get_db)): 
    
    if brt is None:
        raise HTTPException(status_code=500, detail="Boto3 client is not initialized.")
    

    messages = [
        {'role': 'user', 'content': [{'text': request.prompt}]}
    ]

    try:
        response = brt.converse(
            modelId=model_id,
            messages=messages,
            system=aws_system_instructions,
            toolConfig=tool_specifications 
        )

        response_message = response['output']['message']
        messages.append(response_message)

        #Tool-Calling Loop
        while response['stopReason'] == 'tool_use':
            tool_use_blocks = [content for content in response_message['content'] if 'toolUse' in content]
            
            tool_results = []
            
            for block in tool_use_blocks:
                tool_use = block['toolUse']
                tool_name = tool_use['name']
                tool_input = tool_use['input']
                tool_use_id = tool_use['toolUseId']
                
                logger.info(f"Model wants to call tool: {tool_name} with input: {tool_input}")

                if tool_name not in available_tools:
                    tool_results.append({
                        "toolResult": {
                            "toolUseId": tool_use_id,
                            "content": [{"json": {"error": f"Unknown tool: {tool_name}"}}]
                        }
                    })
                    continue

                # Call the actual tool function
                try:
                    tool_function = available_tools[tool_name]
                    # Pass the DB session if the tool function needs it
                    if "db" in tool_function.__code__.co_varnames:
                        tool_output = tool_function(db=db, **tool_input)
                    else:
                        tool_output = tool_function(**tool_input)

                    cleaned_tool_output = json_serialize(tool_output)
                    
                    tool_results.append({
                        "toolResult": {
                            "toolUseId": tool_use_id,
                            "content": [{"json": cleaned_tool_output}]
                        }
                    })
                except Exception as e:
                    logger.error(f"Error executing tool {tool_name}: {e}", exc_info=True)
                    tool_results.append({
                        "toolResult": {
                            "toolUseId": tool_use_id,
                            "content": [{"json": {"error": f"Tool execution failed: {str(e)}"}}]
                        }
                    })

            # Add the tool results to the message history
            messages.append({
                "role": "user",
                "content": tool_results
            })

            #Second API Call (with tool results)
            response = brt.converse(
                modelId=model_id,
                messages=messages,
                system=aws_system_instructions,
                toolConfig=tool_specifications
            )
            response_message = response['output']['message']
            messages.append(response_message)
        
        #Return the Final Text Response ---
        final_text_response = [content['text'] for content in response_message['content'] if 'text' in content]
        
        return {"response": "\n".join(final_text_response)}

    except (ClientError, Exception) as e:
       logger.error(f"ERROR: Can't invoke '{model_id}'. Reason: {e}", exc_info=True)
       raise HTTPException(status_code=500, detail=f"Error conversing with model: {str(e)}")
    

@router.post("/aws_chat_stream/")
def chat_with_aws_stream(request: ChatRequest, db=Depends(get_db)):
    if brt is None:
        raise HTTPException(status_code=500, detail="Boto3 client is not initialized.")
    
    messages = [{'role': 'user', 'content': [{'text': request.prompt}]}]

    try:
        def event_stream():
            """
            Handles streaming conversation with AWS Bedrock, including tool calls.
            Supports partial toolUse deltas.
            """
            while True:
                response_stream = brt.converse_stream(
                    modelId=model_id,
                    messages=messages,
                    system=aws_system_instructions,
                    toolConfig=tool_specifications
                )

                full_response = ""
                current_tool = None
                tool_use_blocks = []
                response_message = None

                for event in response_stream["stream"]:
                    # --- Text token ---
                    if "contentBlockDelta" in event:
                        delta = event["contentBlockDelta"]["delta"]
                        text_part = delta.get("text", "")
                        full_response += text_part
                        yield f"data: {text_part}\n\n"

                    # --- Start of a new assistant message ---
                    elif "messageStart" in event:
                        response_message = {"role": "assistant", "content": []}

                    # --- Start of a new content block (e.g. toolUse) ---
                    elif "contentBlockStart" in event:
                        block = event["contentBlockStart"]["start"]
                        if "toolUse" in block:
                            current_tool = block["toolUse"]
                            current_tool["input"] = {}

                    # --- Streamed deltas updating toolUse input ---
                    elif "contentBlockDelta" in event and "toolUse" in event["contentBlockDelta"]["delta"]:
                        tool_delta = event["contentBlockDelta"]["delta"]["toolUse"]
                        if current_tool:
                            # Merge in streamed fields
                            current_tool["input"].update(tool_delta.get("input", {}))

                    # --- End of a toolUse block ---
                    elif "contentBlockStop" in event:
                        if current_tool:
                            tool_use_blocks.append(current_tool)
                            current_tool = None

                    elif "messageStop" in event:
                        break

                # --- No tool calls → finish ---
                if not tool_use_blocks:
                    yield "data: [END]\n\n"
                    break

                # --- Execute tool calls ---
                tool_results = []
                for tool_use in tool_use_blocks:
                    tool_name = tool_use.get("name")
                    tool_input = tool_use.get("input", {})
                    tool_use_id = tool_use.get("toolUseId")

                    try:
                        if tool_name not in available_tools:
                            result = {"error": f"Unknown tool: {tool_name}"}
                        else:
                            tool_fn = available_tools[tool_name]
                            if "db" in tool_fn.__code__.co_varnames:
                                result = tool_fn(db=db, **tool_input)
                            else:
                                result = tool_fn(**tool_input)

                        cleaned = json_serialize(result)
                        tool_results.append({
                            "toolResult": {
                                "toolUseId": tool_use_id,
                                "content": [{"json": cleaned}]
                            }
                        })

                    except Exception as e:
                        logger.error(f"Error executing tool {tool_name}: {e}", exc_info=True)
                        tool_results.append({
                            "toolResult": {
                                "toolUseId": tool_use_id,
                                "content": [{"json": {"error": str(e)}}]
                            }
                        })

                # Add tool results to conversation
                messages.append({"role": "user", "content": tool_results})

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except (ClientError, Exception) as e:
        logger.error(f"Streaming Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error conversing with model: {str(e)}")