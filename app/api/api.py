from fastapi import FastAPI

from .endpoints import account
from app.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    account.router,
    prefix="/account",
    tags="account"
)
