"""
"""
from pydantic import BaseModel


class OpeningBase(BaseModel):
    """"""

    name: str
    youtube_url: str
    added_by_user: int | None = None


class OpeningAdd(OpeningBase):
    """"""

    pass


class OpeningOut(OpeningBase):
    """."""

    pass


class OpeningInDB(OpeningBase):
    """"""

    id: int
