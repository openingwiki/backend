"""
Dependencies for FastAPI dependency injection system.
"""

from typing import Generator

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
