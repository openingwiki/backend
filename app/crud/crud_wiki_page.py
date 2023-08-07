"""
CRUD requests for wiki_pages.
"""
from app.crud.base import CRUDBase
from app.models import WikiPage
from app.schemas import WikiPageCreate


class CrudWikiPage(CRUDBase[WikiPage, WikiPageCreate]):
    def __init__(self, Model: type[WikiPage]):
        super().__init__(Model)
