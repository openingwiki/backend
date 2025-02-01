"""
Including every router from /endpoints.
app: FastAPI - main variable for backend launching.
"""

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core import settings
from .endpoints import ping, auth, anime, openings

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping")
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(anime.router, prefix="/anime")
api_router.include_router(openings.router, prefix="/openings")

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (can be restrictive)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(api_router, prefix=settings.API_REQUEST_PREFIX)