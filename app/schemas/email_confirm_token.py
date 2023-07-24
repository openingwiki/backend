"""
Email confirm token pydantic models.
"""
from pydantic import BaseModel


class EmailConfirmTokenBase(BaseModel):
    """EmailConfirmToken can be in response and request."""

    token: str


class EmailConfirmTokenIn(EmailConfirmTokenBase):
    """Requests can contain only token."""

    pass


class EmailConfirmTokenOut(EmailConfirmTokenBase):
    """Responses can contain only email confirm token."""

    pass


class EmailConfirmToken(EmailConfirmTokenBase):
    """
    Spicific schema for email confirm token, because there is no sqlalchemy, because it stores in redis.
    Actually, it equals to SqlAlchemy model.
    """

    user_id: int
