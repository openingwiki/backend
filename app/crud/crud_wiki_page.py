"""
CRUD requests for wiki_pages.
"""
from sqlalchemy.orm import Session

from app.models import WikiPage
from app.schemas import WikiPageCreate


def create(db: Session, wiki_page_schema: WikiPageCreate, needs_moderation: bool = True) -> WikiPage:
    """
    Adding wiki page into database.

    Parameters:
        db: Session - db session to deal with.
        wiki_page: schemas.WikiPageCreate - pydantic model for requests with wiki page.
        needs_moderation: bool - flag that wiki page needs to be moderated.

    Returns:
        wiki_page: WikiPage - added wiki_page sqlalchemy model.
    """
    wiki_page_model = WikiPage(
        name=wiki_page_schema.name,
        youtube_url=wiki_page_schema.youtube_url,
        added_by_user=wiki_page_schema.added_by_user,
        needs_moderation=needs_moderation,
    )
    db.add(wiki_page_model)
    db.commit()
    db.refresh(wiki_page_model)
    return wiki_page_model
