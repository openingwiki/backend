from typing import Union
from redis import Redis

from app import schemas
from app.core import security, settings


def create_email_confirm_token(redis: Redis, user: schemas.UserInDB) -> str:
    """
    Creating email confirm token in redis database.

    Parameters:
        redis: Redis - redis database session to deal with.
        user: UserInDB - user pydantic model.

    Returns:
        token: str - email confirmation token.
    """
    email_confirm_token = security.create_access_token()
    redis.set(
        email_confirm_token, user.id, ex=settings.EMAIL_CONFIRM_TOKEN_EXPIRING_SECONDS
    )  # Exires after 3 hours.
    return email_confirm_token


def verify_email_confirm_token(redis: Redis, email_confirm_token: str) -> Union[int, None]:
    """
    Verifying user with token.

    Parameters:
        redis: Redis - redis database session to deal with.
        email_confirm_token: str - token to check.

    Returns:
        None - if there isn't such token.
        user_id - user which email confirm token belongs.
    """
    user_id = redis.get(email_confirm_token)
    if user_id:
        redis.delete(email_confirm_token)
    return user_id
