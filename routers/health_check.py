from fastapi import APIRouter
import logging
from services.cognito.auth import auth
router = APIRouter()
logger = logging.getLogger(__name__)


auth_dep = Depends(auth.claim(Depends(auth.scope(["email", "openid"]))))
router = APIRouter(dependencies=auth_dep)
@router.get("/health", tags=["Health Check"])
def health_check():
    """
    A simple health check endpoint that Docker can call to verify
    if the API is running and ready to accept requests.
    """
    logger.debug("Health check endpoint was called.")
    return {"status": "ok"}
