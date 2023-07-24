from sqlalchemy.orm import Session

from app.crud import crud_access_token
from app.models import AccessToken, User


def random_access_token_indb(db: Session, user: User) -> AccessToken:
    """
    Creating random access token and inserting it into db.

    Parameters:
        db: Session - db session to deal with.
        user: User - user for whom token is creating.

    Returns:
        created_access_token: AccessToken - created access token.
    """
    created_access_token: AccessToken = crud_access_token.create(db, user)
    return created_access_token
