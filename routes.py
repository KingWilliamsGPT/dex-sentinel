from fastapi import APIRouter

from settings import get_settings, get_logger


settings = get_settings()
logger = get_logger(__name__)

router = APIRouter(
    responses = {
        404: {"description": "Not found"},
        403: {"description": "Not authorized"},
    },
)


# Health route for checking if the app is working
@router.get(settings.HEALTH_URL, status_code=204)
async def health_check():
    return

