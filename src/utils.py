from enum import Enum

from sqlalchemy.orm import Session

from schemas import UserCreate, AccessTokenCreate
from core import security, settings
from database import Base, engine
from models import User, AccessToken
from crud import CrudUser, CrudAccessToken


crud_user = CrudUser(User)
crud_access_token = CrudAccessToken(AccessToken)


class Role(Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class OpeningStatus(Enum):
    ON_MODERATION = "moderation"
    ACCEPTED = "accepted"


MOCK_USERS = [
    UserCreate(username="admin", hashed_password=security.get_password_hash("admin"), role=Role.ADMIN),
    UserCreate(username="user", hashed_password=security.get_password_hash("user"), role=Role.USER),
    UserCreate(username="moderator", hashed_password=security.get_password_hash("moderator"), role=Role.MODERATOR)
]
MOCK_ACCESS_TOKENS = [
    AccessTokenCreate(user_id=1, token="1")
]


def init_db(db: Session):
    # Creating database with mock users in test environment.
    if settings.DROP_DATABASE_EVERY_LAUNCH:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        for mock_user in MOCK_USERS:
            crud_user.create(db, mock_user)
        
        for mock_access_token in MOCK_ACCESS_TOKENS:
            crud_access_token.create(db, mock_access_token) 

    else:
        Base.metadata.create_all(bind=engine)


def create_token(db: Session, user: User) -> AccessToken:
    """Utility function to create token"""
    access_token_create = AccessTokenCreate(
        user_id=user.id,
        token=security.create_token(),
    )
    access_token = crud_access_token.create(db, access_token_create)

    return access_token