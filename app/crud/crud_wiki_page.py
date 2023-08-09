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

    def get_last_added(self, db: Session, limit: int) -> list[WikiPage]:
        """
        Getting last added wiki pages.

        Parameters:
            db: Session - db session to deal with.
            limit: int - count of last added wiki pages.

        Returns:
            last_added_wiki_pages: list[WikiPage] - list of WikiPages.
        """
        return db.query(WikiPage).filter(WikiPage.is_moderated == True).order_by(WikiPage.added_at).limit(limit).all()

    def get_unmoderated(self, db: Session, limit: int) -> list[WikiPage]:
        """
        Getting unmoderated wiki pages.

        Parameters:
            db: Session - db session to deal with.
            limit: int - count of needed unmoderated wiki pages.

        Returns:
            unmoderated_wiki_pages: list[WikiPage] - list of WikiPages.
        """
        return db.query(WikiPage).filter(WikiPage.is_moderated == False).order_by(WikiPage.added_at).limit(limit).all()

    def set_moderated(self, db: Session, wiki_page: WikiPage) -> WikiPage:
        """
        Setting moderated status to wiki page.
        """
        wiki_page.is_moderated = True
        db.commit()
        db.refresh(wiki_page)
        return wiki_page
