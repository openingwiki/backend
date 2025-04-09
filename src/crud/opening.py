"""
CRUD requests for the openings.
"""
from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import func

from crud.base import CrudBase
from models import Opening
from schemas import OpeningCreate, OpeningUpdate


class CrudOpening(CrudBase[Opening, OpeningCreate, OpeningUpdate]):
    def __init__(self, Model: type[Opening]):
        super().__init__(Model)

    def is_opening(self, db: Session, opening_id: int):
        return self.get(db, opening_id) != None

    def get_by_limit_and_offset(self, db: Session, limit: int = 10, offset: int = 0) -> list[Opening]:
        return db.query(Opening).limit(limit).offset(offset).all()

    def search(self, db: Session, query: str, limit: int = 10, offset: int = 0) -> list[Opening]:
        return (
            db.query(Opening)
            .filter(Opening.name.ilike(f"%{query}%"))
            .limit(limit)
            .offset(offset)
            .all()
        )
    
    def get_total_number(self, db: Session) -> int:
        return db.query(func.count(Opening.id)).scalar()

    def get_search_total_number(self, db: Session, query: str) -> int:
        return (
            db.query(func.count(Opening.id))
            .filter(Opening.name.ilike(f"%{query}%"))
            .scalar()
        )