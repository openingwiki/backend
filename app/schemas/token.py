"""
Pydantic token models.
"""
from pydantic import BaseModel


class TokenBase(BaseModel):
    """Token can be in response and request."""

    token: str


class TokenIn(TokenBase):
    """Requests can contain only token."""

    pass


class TokenOut(TokenBase):
    """Responses can contain only token."""

    pass


class TokenInDB(TokenBase):
    """Token in db also stores whose is token."""

    token_id: int
    account_id: int
