"""
User pydantic models.
"""
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Every user model must contain email."""

    email: EmailStr


class UserIn(UserBase):
    password: str


class UserCreate(UserIn):
    """Schema for adding into database."""

    nickname: str


class UserLogin(UserIn):
    """Schema for login."""

    pass


class UserOut(UserBase):
    """Response information about user."""

    id: int
    verified: bool
