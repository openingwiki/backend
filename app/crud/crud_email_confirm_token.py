from typing import Union

from redis import Redis

from app.core import settings
from app.schemas import EmailConfirmToken, EmailConfirmTokenCreate


class CRUDEmailConfirmToken:
    def __init__(self) -> None:
        pass

    def create(self, redis: Redis, email_confirm_token: EmailConfirmTokenCreate) -> EmailConfirmToken:
        """
        Creating email confirm token in redis database.

        Parameters:
            redis: Redis - redis database session to deal with.
            user: UserInDB - user pydantic model.

        Returns:
            email_confirm_token: EmailConfirmToken - email confirmation token pydantic schema.
        """
        redis.set(
            email_confirm_token.token, email_confirm_token.user_id, ex=settings.EMAIL_CONFIRM_TOKEN_EXPIRING_SECONDS
        )  # Expires after 3 hours.
        return email_confirm_token

    def verify(self, redis: Redis, email_confirm_token: str) -> Union[int, None]:
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
        return user_id
