"""
CRUD requests for access token.
"""
from typing import Union

from sqlalchemy.orm import Session

from app.core import security
from app.models import AccessToken, User
from app.utils import return_converter


@return_converter
def create(db: Session, user: User) -> AccessToken:
    """
    Creating access token.

    Parameters:
        db: Session - database session to deal with.
        access_token: AccessToken - pydantic model of access token.

    Returns:
        access_token: str - created access token.
    """
    token = security.create_token()
    created_access_token = AccessToken(token=token, user_id=user.id)
    db.add(created_access_token)
    db.commit()
    db.refresh(created_access_token)
    return created_access_token


@return_converter
def get(db: Session, access_token: str) -> Union[AccessToken, None]:
    """
    Getting acces access token row from table by access token.

    Parameters:
        db: Session - database session to deal with.
        access_token: str - access token.

    Returns:
        access_token_model: AccessToken - access token sqlalchemt model.
        None if there isn't such access token.
    """
    return db.query(AccessToken).filter(AccessToken.token == access_token).first()
