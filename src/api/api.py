"""
Including every router from /endpoints.
app: FastAPI - main variable for backend launching.
"""

from fastapi import APIRouter, FastAPI

from core import settings
from .endpoints import ping

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping")

app = FastAPI()
app.include_router(api_router, prefix=settings.API_REQUEST_PREFIX)