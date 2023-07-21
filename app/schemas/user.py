"""
User pydantic models.
"""
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """Every user model must contain email."""

    email: EmailStr


class UserIn(UserBase):
    password: str


class UserCreate(UserIn):
    """There is password for requests."""

    nickname: str


class UserLogin(UserIn):
    """There is password for requests."""

    pass


class UserInDB(UserBase):
    """How user storing in DB."""

    # Model settings.
    model_config = ConfigDict(from_attributes=True)

    id: int
    hashed_password: str
    verified: bool
    avatar_path: str
    is_moderator: bool
    is_admin: bool


class UserOut(UserBase):
    """
    Response information about user.
    Password can't be in response.
    """

    id: int
    verified: bool
