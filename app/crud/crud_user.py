"""
CRUD requests for user.
"""
from typing import Union

from sqlalchemy.orm import Session

from app.core import security
from app.models import User
from app.schemas import UserCreate
from app.utils import return_converter


@return_converter
def create(db: Session, user: UserCreate) -> User:
    """
    Adding user into table.

    Parameters:
        db: Session - db session to deal with.
        user: UserIn - user pydantic model.

    Returns:
        user_model: UserInDB - SQLAlchemy model with user data.
    """
    user_hashed_password = security.get_password_hash(user.password)
    user_model = User(email=user.email, hashed_password=user_hashed_password, verified=False, nickname=user.nickname)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model


@return_converter
def get(db: Session, user_id: int) -> Union[User, None]:
    """
    Getting user from table by user id.

    Parameters:
        db: Session - db session to deal with.
        user_id: int - user id of user to get.

    Returns:
        user: user - SQLAlchemy model with user data.
        None - if there isn't such user.
    """
    return db.query(User).filter(User.id == user_id).first()


@return_converter
def get_by_email(db: Session, email: str) -> Union[User, None]:
    """
    Getting user from table by email.

    Parameters:
        db: Session - db session to deal with.
        email: int - email of user ot get.

    Returns:
        user: User - SQLAlchemy model with user data.
        None - if there isn't such user.
    """
    return db.query(User).filter(User.email == email).first()


@return_converter
def set_moderator(db: Session, user: User) -> User:
    """
    Setting user to moderator.
    """
    user.is_moderator = True
    db.commit()
    db.refresh(user)
    return user


@return_converter
def verify(db: Session, user: User) -> User:
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
    db.refresh(user)
    return user
