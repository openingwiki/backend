"""
CRUD requests for wiki_pages.
"""
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import WikiPage
from app.schemas import WikiPageCreate


class CRUDWikiPage(CRUDBase[WikiPage, WikiPageCreate]):
    def __init__(self, Model: type[WikiPage]):
        super().__init__(Model)

    def get_last_added(self, db: Session, limit: int = 1) -> list[WikiPage]:
        """
        Getting last added wiki pages.

        Parameters:
            db: Session - db session to deal with.
            limit: int - count of last added wiki pages.

        Returns:
            last_added_pages: list[WikiPage] - list of WikiPages.
        """
        return (
            db.query(WikiPage).filter(WikiPage.needs_moderation == False).order_by(WikiPage.added_at).limit(limit).all()
        )
