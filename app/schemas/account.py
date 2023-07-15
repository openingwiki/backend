from pydantic import BaseModel, EmailStr


class AccountBase(BaseModel):
    email: EmailStr


class AccountIn(AccountBase):
    password: str


class AccountInDB(AccountBase):
    account_id: int
    hashed_password: str
    verified: bool

    class Config:
        from_attributes = True


class AccountOut(AccountBase):
    verified: bool