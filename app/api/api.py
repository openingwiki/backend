"""
Including every router from /endpoints.
app: FastAPI - main variable for backend launching.
"""

from fastapi import FastAPI

from .endpoints import user, openings
from app.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(openings.router, prefix="/openings", tags=["openings"])
