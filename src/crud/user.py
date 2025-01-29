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

    def get_by_login(self, db: Session, login: str) -> User | None:
        """
        Get user by login.

        Parameters:
            db: Session - db session to deal with.
            login: str - login of the user to get.

        Return:
            user: User - user sqlalchemy model.
        """
        return db.query(User).filter(User.login == login).first()

