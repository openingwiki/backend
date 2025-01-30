"""
Dependencies for FastAPI dependency injection system.
"""
from typing import Generator, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User, AccessToken
from crud import CrudAccessToken, CrudUser


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
crud_access_token = CrudAccessToken(AccessToken)
crud_user = CrudUser(User)


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


def get_current_user(
    access_token_str: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> User:
    """
    This dependency injection used for getting user,
    which has sent requests with access token.
    Token must be passed in headers.

    Parameters:
        token: Annotated[str, Depends(oatuh2_scheme)] - access token from headers.
        db: Session - SQLAlchemy session to database, initializing in dependency injection.

    Returns:
        user: models.User - user sqlalchemy model.
        HTTPExecption(401) if invalid access token.
    """
    access_token: AccessToken = crud_access_token.get_by_token(db, access_token_str)
    if not access_token:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Invalid access token."
        )

    return access_token.user