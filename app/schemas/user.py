"""
User pydantic models.
"""
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Every user model must contain email."""

    email: EmailStr


class UserAuth(UserBase):
    password: str


class UserRegister(UserAuth):
    """Schema for getting register request."""

    nickname: str


class UserCreate(UserBase):
    """Schema for adding into database."""

    nickname: str
    hashed_password: str


class UserLogin(UserAuth):
    """Schema for login."""

    pass


class UserOut(UserBase):
    """Response information about user."""

    id: int
    verified: bool
