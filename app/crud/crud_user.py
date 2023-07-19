"""
CRUD requests for user.
"""
from sqlalchemy.orm import Session
from typing import Union

from app import models
from app import schemas
from app.core import security


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Adding user into table.

    Parameters:
        db: Session - db session to deal with.
        user: UserIn - user pydantic model.

    Returns:
        user_model: UserInDB - SQLAlchemy model with user data.
    """
    user_hashed_password = security.get_password_hash(user.password)
    user_model = models.User(email=user.email, hashed_password=user_hashed_password, verified=False)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model


def get_user(db: Session, user_id: int) -> Union[models.User, None]:
    """
    Getting user from table by user id.

    Parameters:
        db: Session - db session to deal with.
        user_id: int - user id of user to get.

    Returns:
        user: user - SQLAlchemy model with user data.
        None - if there isn't such user.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Union[models.User, None]:
    """
    Getting user from table by email.

    Parameters:
        db: Session - db session to deal with.
        email: int - email of user ot get.

    Returns:
        user: User - SQLAlchemt model with user data.
        None - if there isn't such user.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def verify_user(db: Session, user: models.User):
    """
    Setting user verified flag to True.

    Parameters:
        db: Session - db session to deal with.
        user: User - user SQLAlchemy model.

    Returns
        Nothing
    """
    user.verified = True
    db.commit()
