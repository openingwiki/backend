"""
CRUD requests for the users.
"""

from sqlalchemy.orm import Session

from crud.base import CrudBase
from models import User
from schemas import UserCreate, UserUpdate


class CrudUser(CrudBase[User, UserCreate, UserUpdate]):
    def __init__(self, Model: type[User]):
        super().__init__(Model)

    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def is_username(self, db: Session, username: str) -> User | None:
        return self.get_by_username(db, username) != None    
