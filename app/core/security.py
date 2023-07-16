import secrets
from passlib.context import CryptContext

from app.core import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(token_lenght: int) -> str:
    return secrets.token_hex(token_lenght)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password + settings.PASSWORD_SALT, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password + settings.PASSWORD_SALT)

