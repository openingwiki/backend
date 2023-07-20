"""
Dependencies for FastAPI dependency injection system.
"""

from typing import Annotated, Generator

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.crud import crud_access_token, crud_user
from app.db import SessionLocal
from app.redis import open_connection


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
    """
    This dependency injection used for getting user, which has sent requests with token.
    Token must be stored in cookies.

    Parameters:
        token: Annotated[str, Cookie()] - token from cookie.
        db: Session - SQLAlchemy session to database, initializing in dependency injection.

    Returns:
        user: models.User - user sqlalchemy model.
        HTTPExecption(401) if invalid token.  
    """
    token_data: models.Token = crud_access_token.get_access_token_info(db, token)

    if not token_data:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")

    user = crud_user.get_user(db, user_id=token_data.user_id)

    return user
