"""
Access token pydantic models.
"""

from datetime import datetime

from pydantic import BaseModel


class AccessTokenCreate(BaseModel):
    user_id: int
    token: str


class AccessTokenOut(BaseModel):
    token: str


class AccessTokenUpdate(BaseModel):
    pass