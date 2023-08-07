"""
WikiPage pydantic models.
"""
from pydantic import BaseModel


class WikiPageBase(BaseModel):
    """WikiPage base model."""

    name: str
    youtube_url: str


class WikiPageCreate(WikiPageBase):
    """WikiPage body in request."""

    added_by_user: int | None = None
    needs_moderation: bool = True


class WikiPageIn(WikiPageBase):
    """Wiki page in."""

    pass


class WikiPageOut(WikiPageBase):
    """WikiPage in response."""

    id: int
