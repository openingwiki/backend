from pydantic import BaseModel


class UserRegistration(BaseModel):
    username: str 
    password: str


class UserCreate(BaseModel):
    username: str
    hashed_password: str


class UserAuth(BaseModel):
    login: str
    password: str


class UserUpdate(BaseModel):
    pass


class UserOut(BaseModel):
    id: int
    username: str
