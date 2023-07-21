"""
WikiPage pydantic models.
"""
from pydantic import BaseModel


class WikiPageBase(BaseModel):
    """WikiPage base model."""

    name: str
    youtube_url: str
    added_by_user: int | None = None


class WikiPageCreate(WikiPageBase):
    """WikiPage body in request."""

    pass


class WikiPageOut(WikiPageBase):
    """WikiPage in response."""

    pass


class WikiPageInDB(WikiPageBase):
    """WikiPage in db."""

    id: int
