from fastapi import APIRouter
import logging
router = APIRouter()
logger = logging.getLogger(__name__)


router = APIRouter()
@router.get("/health", tags=["Health Check"])
def health_check():
    """
    A simple health check endpoint that Docker can call to verify
    if the API is running and ready to accept requests.
    """
    logger.debug("Health check endpoint was called.")
    return {"status": "ok"}
