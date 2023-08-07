"""
Access token pydantic models.
"""
from pydantic import BaseModel


class AccessTokenBase(BaseModel):
    """AccessToken can be in response and request."""

    token: str


class AccessTokenIn(AccessTokenBase):
    """Requests can contain only token."""

    pass


class AccessTokenOut(AccessTokenBase):
    """Responses can contain only token."""

    pass


class AccessTokenCreate(AccessTokenBase):
    """Acces token for cruds."""

    user_id: int
