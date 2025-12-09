from fastapi_cloudauth.cognito import Cognito
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

aws_region = "us-east-2"
userPoolId = ""
client_id = ""

auth = Cognito(
    region=aws_region, 
    userPoolId=userPoolId,
    client_id=client_id
)
