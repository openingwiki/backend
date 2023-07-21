"""
Including every router from /endpoints.
app: FastAPI - main variable for backend launching.
"""

from fastapi import FastAPI

from .endpoints import user, wiki_pages

app = FastAPI()

app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(wiki_pages.router, prefix="/wiki_pages", tags=["wiki_pages"])
