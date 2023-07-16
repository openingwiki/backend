"""
Function for security like password hashing and etc.
"""

import secrets
from passlib.context import CryptContext

from app.core import settings
from app import schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token() -> str:
    """
    Generating random token.

    Parameters:
        token_lenght: int - token lenght in bytes count. So actually token lenght will token_lenght * 2 symbols.

    Returning:
        token: str - generated token.
    """
    token = secrets.token_hex(settings.TOKEN_LENGHT_IN_BYTES)
    return token


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifying password.
    Calculating hash with salt again.
    If hashes are equal, then password is correct.

    Parameters:
        plain_password: str - password to check.
        hashed_password: str - hashed password to compare.

    Returns:
        is_right: bool - boolean that entered password hash is equal with hash.
    """
    return pwd_context.verify(plain_password + settings.PASSWORD_SALT, hashed_password)


def get_password_hash(plain_password: str) -> str:
    """
    Generating password hash from plain password.

    Parameters:
        plain_password: str - clean password.

    Returns:
        password_hash: str - password hash.
    """
    return pwd_context.hash(plain_password + settings.PASSWORD_SALT)
