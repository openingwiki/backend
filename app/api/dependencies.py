"""
Dependencies for FastAPI dependency injection system.
"""

from typing import Generator, Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, Cookie, HTTPException

from app.db import SessionLocal
from app.redis import open_connection
from app.crud import crud_token, crud_user
from app import models


def get_db() -> Generator:
    """
    This dependency injection used for creating db session.
    Db session closes after FastAPI query completion.

    Parameters:
        Nothing.

    Returns:
        db: Session - database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_redis() -> Generator:
    """
    This dependency injection used for creating redis session.
    Redis session closes after FastAPI query completion.

    Parameters:
        Nothing.

    Returns:
        redis: Redis - redis session.
    """
    try:
        redis = open_connection()
        yield redis
    finally:
        redis.close()


def get_current_user(token: Annotated[str, Cookie()], db: Session = Depends(get_db)) -> models.User:
    token_data: models.Token = crud_token.get_token(db, token)

    if not token_data:
        raise HTTPException(403, detail="Invalid token.")

    user = crud_user.get_user(db, user_id=token_data.user_id)

    return user
