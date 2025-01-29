"""
Dependencies for FastAPI dependency injection system.
"""

from typing import Generator

from fastapi.security import OAuth2PasswordBearer

from database import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
