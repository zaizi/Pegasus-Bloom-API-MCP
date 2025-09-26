import google.generativeai as genai
from google.generativeai.types import Tool
from google.generativeai.protos import FunctionResponse
import os
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from mcp.types import TextContent
import logging
from tools.declarations import summarise_csv, company_information, retrieve_from_knowledge_base
from dotenv import load_dotenv
import asyncio


load_dotenv()
logger = logging.getLogger(__name__)
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")


def create_gemini_model():
    try:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=gemini_api_key)

        summarise_csv_file_tool_declaration = summarise_csv.summarise_csv_file_tool_declaration
        company_profile_declaration = company_information.get_company_profile_declaration
        list_competitors_declaration = company_information.list_available_competitors_explicit
        company_officers_declaration = company_information.get_company_officers_declaration
        person_significant_control_declaration = company_information.get_person_significant_control_declaration
        latest_filing_declaration = company_information.get_company_latest_filing_declaration
        company_charges_declaration = company_information.get_company_charges_declaration
        search_by_sic_declaration = company_information.get_search_by_sic_code_declaration
        retrieve_from_knowledge_base_declaration = retrieve_from_knowledge_base.rag_retriever


        gemini_tools = [
                        Tool(function_declarations=[summarise_csv_file_tool_declaration, 
                                                    company_profile_declaration, 
                                                    list_competitors_declaration,
                                                    company_officers_declaration,
                                                    person_significant_control_declaration,
                                                    latest_filing_declaration,
                                                    company_charges_declaration,
                                                    search_by_sic_declaration,
                                                    retrieve_from_knowledge_base_declaration
                                                    ]
                            )
                        ]
        
        system_instructions = """If you do not need to run tool calls, begin the response with a concise direct answer to the prompt's main question.

                                If you have used a tool and received a list or dictionary as a response, do not output the raw dictionary or list. 
                                Instead, process the data and present the most important information in a user-friendly summary. 
                                Use bullet points or a simple table for clarity, and explain what the findings mean in a natural, helpful tone.

                                Structure the response logically. Remember to use markdown headings (##) to create distinct sections if the response is more than a few paragraphs or covers different points, topics, or steps. 
                                If a response uses markdown headings, add horizontal lines to separate sections. Prioritize coherence over excessive fragmentation.

                                Use relevant emojis when appropriate 💡. 
                                Ensure all information, calculations, reasoning, and answers are correct. 
                                Provide complete answers addressing all parts of the prompt, but be brief and informative, avoiding unnecessary details or redundancy.
                                """

        model = genai.GenerativeModel(
            # Using a recommended model name. "gemini-2.0-flash" is not a public model.
            model_name="gemini-1.5-flash",
            tools=gemini_tools,
            system_instruction=system_instructions
        )
        return model
    

    except Exception as e:
        logger.error(f"Failed to create Gemini model: {e}", exc_info=True)
        return None


def call_mcp_server_tool(tool_name: str, args: dict) -> dict:
    
    logger.debug(f"Calling MCP server tool '{tool_name}' with args: {args}")

    async def inner_call():
        transport = StreamableHttpTransport(url=MCP_SERVER_URL)
        async with Client(transport=transport) as client:
            result = await client.call_tool(tool_name, args)
            return result
    try:
        return asyncio.run(inner_call())
    except Exception as e:
        logger.error(f"Error communicating with MCP server tool '{tool_name}'", exc_info=True)
        return {"error": f"MCP Server Tool Error: {e}"}



def handle_gemini_response(chat_session, initial_gemini_response):
    """
    Processes Gemini's response, handling tool calls and ensuring the
    response format is always a dictionary before sending back to the model.
    """
    response = initial_gemini_response
    
    while True:
        part = response.parts[0]

        if part.text:
            logger.info(f"Gemini returned final text: {part.text}")
            return part.text

        if not part.function_call:
            logger.warning("Gemini response had no text and no function call. Exiting.")
            return "The model did not provide a text response."

        function_call = part.function_call
        tool_name = function_call.name
        args = {key: value for key, value in function_call.args.items()}
        logger.debug(f"Gemini wants to call: {tool_name} with args: {args}")    
    

        logger.info(f"Calling generic tool: {tool_name}")
        tool_output = call_mcp_server_tool(tool_name, args)
        logger.debug(f"Received tool output: {tool_output}")
        response_data = {}
        if isinstance(tool_output, dict):
            # If it's already a dictionary, use it directly.
            response_data = tool_output
        elif isinstance(tool_output, list):
            # If it's a list, convert it to a dictionary.
            response_data = {"result": str(tool_output)}
            logger.info(f"Converted list output to dict: {response_data}")
        else:
            # Handle any other unexpected types gracefully.
            response_data = {"error": "Received an unexpected output format from the tool.", "details": str(tool_output)}
            logger.warning(f"Unexpected tool output format: {type(tool_output)}")

        # Send the guaranteed-to-be-a-dictionary back to the model
        response = chat_session.send_message(
            FunctionResponse(name=tool_name, response=response_data)
        )
