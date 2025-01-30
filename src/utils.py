from enum import Enum

from sqlalchemy.orm import Session

from schemas import UserCreate
from core import security, settings
from database import Base, engine
from models import User
from crud import CrudUser


class Role(Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


MOCK_USERS = [
    UserCreate(username="admin", hashed_password=security.get_password_hash("admin"), role=Role.ADMIN),
    UserCreate(username="user", hashed_password=security.get_password_hash("user"), role=Role.USER),
    UserCreate(username="moderator", hashed_password=security.get_password_hash("moderator"), role=Role.MODERATOR)
]


def init_db(db: Session):
    # Creating database with mock users in test environment.
    if settings.DROP_DATABASE_EVERY_LAUNCH:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        crud_user = CrudUser(User)

        for mock_user in MOCK_USERS:
            crud_user.create(db, mock_user)

    else:
        Base.metadata.create_all(bind=engine)


