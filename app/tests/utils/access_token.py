from sqlalchemy.orm import Session

from app.core import security
from app.crud import crud_access_token
from app.models import AccessToken, User
from app.schemas import AccessTokenCreate


def random_pydantic_access_token_create(user: User) -> AccessTokenCreate:
    access_token_create = AccessTokenCreate(user_id=user.id, token=security.create_token())
    return access_token_create


def random_access_token_indb(db: Session, user: User) -> AccessToken:
    """
    Creating random access token and inserting it into db.

    Parameters:
        db: Session - db session to deal with.
        user: User - user for whom token is creating.

    Returns:
        created_access_token: AccessToken - created access token.
    """
    access_token_create = random_pydantic_access_token_create(user)
    created_access_token: AccessToken = crud_access_token.create(db, access_token_create)
    return created_access_token
