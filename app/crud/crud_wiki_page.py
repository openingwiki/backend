"""
CRUD requests for wiki_pages.
"""
from typing import Union

from sqlalchemy.orm import Session

from app import models, schemas


def add_wiki_page(db: Session, wiki_page: schemas.WikiPageAdd, needs_moderation: bool = True) -> models.WikiPage:
    """
    Adding wiki page into database.

    Parameters:
        db: Session - db session to deal with.
        wiki_page: schemas.WikiPageAdd - pydantic model for requests with wiki page.
        needs_moderation: bool - flag that wiki page needs to be moderated.

    Returns:
        models.WikiPage - added wiki_page sqlalchemy model.
    """
    wiki_page_model = models.WikiPage(
        name=wiki_page.name,
        youtube_url=wiki_page.youtube_url,
        added_by_user=wiki_page.added_by_user,
        needs_moderation=needs_moderation,
    )
    db.add(wiki_page_model)
    db.commit()
    db.refresh(wiki_page_model)
    return wiki_page_model
