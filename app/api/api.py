"""
Including every router from /endpoints.
app: FastAPI - main variable for backend launching.
"""

from fastapi import APIRouter

from .endpoints import user, wiki_page

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(wiki_page.router, prefix="/wiki_page", tags=["wiki_page"])
