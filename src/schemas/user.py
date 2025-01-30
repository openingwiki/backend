from pydantic import BaseModel

from core import security


class UserRegistration(BaseModel):
    username: str 
    password: str


class UserCreate(BaseModel):
    username: str
    hashed_password: str

    @classmethod
    def convert_from_user_registration(cls, user_data: UserRegistration):
        return cls(
            username=user_data.username,
            hashed_password=security.get_password_hash(user_data.password),
        )

class UserAuth(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    pass


class UserOut(BaseModel):
    id: int
    username: str
