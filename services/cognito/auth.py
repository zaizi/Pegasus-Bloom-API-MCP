from fastapi_cloudauth.cognito import Cognito
from dotenv import load_dotenv
import logging
from os import getenv
load_dotenv()
logger = logging.getLogger(__name__)

aws_region = getenv(key="aws_region", default="eu-east-2")
userPoolId = getenv(key="userPoolId", default=None)
client_id = getenv(key="client_id", default=None)

auth = Cognito(
    region=aws_region, 
    userPoolId=userPoolId,
    client_id=client_id
)
