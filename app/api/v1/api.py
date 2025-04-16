from fastapi import APIRouter

from app.core.config import get_settings
from app.api.v1.endpoints import pastes

# Get settings
settings = get_settings()

# Create API router
api_router = APIRouter(prefix=settings.API_V1_PREFIX)

# Include endpoints
api_router.include_router(pastes.router) 