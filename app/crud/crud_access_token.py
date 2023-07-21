"""
CRUD requests for token.
"""
from typing import Union

from sqlalchemy.orm import Session

from app import models
from app.core import security


def create(db: Session, user: models.User) -> models.Token:
    """
    Creating token.

    Parameters:
        db: Session - database session to deal with.
        user: models.User - pydantic model of user for which the token is being created.

    Returns:
        token: str - created token.
    """
    token = security.create_token()
    token_model = models.Token(token=token, user_id=user.id)
    db.add(token_model)
    db.commit()
    db.refresh(token_model)
    return token_model


def get(db: Session, token: str) -> Union[models.Token, None]:
    """
    Getting acces token row from table by token.

    Parameters:
        db: Session - database session to deal with.
        token: str - token.

    Returns:
        token_model: models.Token - token sqlalchemt model.
        None if there isn't such token.
    """
    return db.query(models.Token).filter(models.Token.token == token).first()
