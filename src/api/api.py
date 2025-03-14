"""
Including every router from /endpoints.
app: FastAPI - main variable for backend launching.
"""

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core import settings
from .endpoints import ping, auth, anime, openings, users

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping")
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(anime.router, prefix="/anime")
api_router.include_router(openings.router, prefix="/openings")
api_router.include_router(users.router, prefix="/users")

app = FastAPI()


origins = [
    "http://localhost:3000",  # Vite (Vue 3) default dev server
    "http://127.0.0.1:3000",  
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           
    allow_credentials=True,          
    allow_methods=["GET", "POST", "PUT", "DELETE"],   
    allow_headers=["*"],             
)

app.include_router(api_router, prefix=settings.API_REQUEST_PREFIX)