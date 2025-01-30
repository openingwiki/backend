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
    