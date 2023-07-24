from typing import Type, Union

from pydantic import BaseModel
from redis import Redis
from sqlalchemy.orm import Session

from app.core import security, settings
from app.crud import crud_user
from app.models import User
from app.schemas import EmailConfirmToken
from app.utils import return_converter


@return_converter
def create(redis: Redis, user: User) -> EmailConfirmToken:
    """
    Creating email confirm token in redis database.

    Parameters:
        redis: Redis - redis database session to deal with.
        user: UserInDB - user pydantic model.

    Returns:
        email_confirm_token: EmailConfirmToken - email confirmation token pydantic schema.
    """
    email_confirm_token = EmailConfirmToken(token=security.create_token(), user_id=user.id)
    redis.set(
        email_confirm_token.token, email_confirm_token.user_id, ex=settings.EMAIL_CONFIRM_TOKEN_EXPIRING_SECONDS
    )  # Expires after 3 hours.
    return email_confirm_token


@return_converter
def verify(db: Session, redis: Redis, email_confirm_token: str) -> Union[User, None]:
    """
    Verifying user with token.

    Parameters:
        db: Session - database session to deal with.
        redis: Redis - redis database session to deal with.
        email_confirm_token: str - token to check.

    Returns:
        None - if there isn't such token.
        user_id - user which email confirm token belongs.
    """
    user_id: int = redis.get(email_confirm_token)
    if not user_id:
        return None

    redis.delete(email_confirm_token)
    user: User = crud_user.get(db, user_id)
    return user
