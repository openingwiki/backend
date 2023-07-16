from pydantic import BaseModel


class TokenBase(BaseModel):
    token: str


class TokeIn(TokenBase):
    pass


class TokeOut(TokenBase):
    pass


class TokeInDB(TokenBase):
    token_id: int
    account_id: int