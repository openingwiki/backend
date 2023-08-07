"""
Including every router from /endpoints.
app: FastAPI - main variable for backend launching.
"""

from fastapi import APIRouter

from .endpoints import user, wiki_pages

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(wiki_pages.router, prefix="/wiki_pages", tags=["wiki_pages"])
