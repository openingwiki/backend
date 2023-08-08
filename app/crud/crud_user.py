"""
CRUD requests for user.
"""
from typing import Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas import UserCreate


class CRUDUser(CRUDBase[User, UserCreate]):
    def __init__(self, Model: type[User]):
        super().__init__(Model)

    def get_by_email(self, db: Session, email: str) -> Union[User, None]:
        """
        Getting user from table by email.

        Parameters:
            db: Session - db session to deal with.
            email: str - email of user to get.

        Returns:
            user: User - SQLAlchemy model with user data.
            None - if there isn't such user.
        """
        return db.query(User).filter(User.email == email).first()

    def get_by_nickname(self, db: Session, nickname: str) -> Union[User, None]:
        """
        Getting user from table by nickname.

        Parameters:
            db: Session - db session to deal with.
            nickname: str - nickname of user to get.

        Returns:
            user: User - SQLAlchemy model with user data.
            None - if there isn't such user.
        """
        return db.query(User).filter(User.nickname == nickname).first()

    def set_moderator(self, db: Session, user: User) -> User:
        """
        Setting user to moderator.
        """
        user.is_moderator = True
        db.commit()
        db.refresh(user)
        return user

    def verify(self, db: Session, user: User) -> User:
        """
        Setting user verified flag to True.

        Parameters:
            db: Session - db session to deal with.
            user: User - user SQLAlchemy model.

        Returns
            Nothing
        """
        user.verified = True
        db.commit()
        db.refresh(user)
        return user

    def is_user_email(self, db: Session, email: str) -> bool:
        """"""
        user: User | None = self.get_by_email(db, email)
        return bool(user)

    def is_user_nickname(self, db: Session, nickname: str) -> bool:
        user: User | None = self.get_by_nickname(db, nickname)
        return bool(user)
