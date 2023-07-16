"""
Pydantic account models.
"""
from pydantic import BaseModel, EmailStr


class AccountBase(BaseModel):
    """Every account model must contain email."""

    email: EmailStr


class AccountIn(AccountBase):
    """There is password for requests."""

    password: str


class AccountInDB(AccountBase):
    """How account stored in DB."""

    account_id: int
    hashed_password: str
    verified: bool

    class Config:
        from_attributes = True


class AccountOut(AccountBase):
    """
    Response information about Account.
    Password can't be in response.
    """

    account_id: int
    verified: bool
