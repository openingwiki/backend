"""
CRUD requests for the openings.
"""

from sqlalchemy.orm import Session

from crud.base import CrudBase
from models import Opening
from schemas import OpeningCreate, OpeningUpdate


class CrudOpening(CrudBase[Opening, OpeningCreate, OpeningUpdate]):
    def __init__(self, Model: type[Opening]):
        super().__init__(Model)

    def is_opening(self, db: Session, opening_id: int):
        return self.get(db, opening_id) != None