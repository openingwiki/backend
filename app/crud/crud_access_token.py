"""
CRUD requests for access token.
"""
from typing import Union

from sqlalchemy.orm import Session

from app import models
from app.core import security


def create(db: Session, access_token: models.AccessToken) -> models.AccessToken:
    """
    Creating access token.

    Parameters:
        db: Session - database session to deal with.
        access_token: models.AccessToken - pydantic model of access token.

    Returns:
        access_token: str - created access token.
    """
    db.add(access_token)
    db.commit()
    db.refresh(access_token)
    return access_token


def get(db: Session, access_token: str) -> Union[models.AccessToken, None]:
    """
    Getting acces access token row from table by access token.

    Parameters:
        db: Session - database session to deal with.
        access_token: str - access token.

    Returns:
        access_token_model: models.Token - access token sqlalchemt model.
        None if there isn't such access token.
    """
    return db.query(models.AccessToken).filter(models.AccessToken.token == access_token).first()
