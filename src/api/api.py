"""
Including every router from /endpoints.
app: FastAPI - main variable for backend launching.
"""

from fastapi import APIRouter, FastAPI

from core import settings
from .endpoints import ping, auth, anime, openings

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping")
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(anime.router, prefix="/anime")
api_router.include_router(openings.router, prefix="/openings")

app = FastAPI()
app.include_router(api_router, prefix=settings.API_REQUEST_PREFIX)