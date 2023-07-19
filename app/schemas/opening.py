"""
Opening pydantic models.
"""
from pydantic import BaseModel


class OpeningBase(BaseModel):
    """Opening base model."""

    name: str
    youtube_url: str
    added_by_user: int | None = None


class OpeningAdd(OpeningBase):
    """Opening body in request."""

    pass


class OpeningOut(OpeningBase):
    """Opening in response."""

    pass


class OpeningInDB(OpeningBase):
    """Opening in db."""

    id: int
