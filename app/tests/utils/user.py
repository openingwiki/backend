from sqlalchemy.orm import Session

from app.core import security
from app.crud import crud_user
from app.models import User
from app.schemas import UserCreate


def random_pydantic_user_create() -> UserCreate:
    """
    Random pydantic user create.

    Parameters:
        nothing.

    Returns:
        pydantic_user_create: UserCreate - random pydantic user create model.
    """
    pydantic_user_create = UserCreate(
        email="forspam@gmail.com", nickname="DarkFlameMaster", hashed_password=security.get_password_hash("password")
    )
    return pydantic_user_create


def random_user_indb(db: Session) -> User:
    """
    Creating random user and inserting it into db.

    Parameters:
        db: Session - database session to deal with.

    Returns:
        created_user: User - created user.
    """
    random_user = random_pydantic_user_create()
    created_user: User = crud_user.create(db, random_user)
    return created_user


def random_moderator_indb(db: Session) -> User:
    """
    Creating random user and inserting it into db with moderator privilegies.

    Parameters:
        db: Session - database session to deal with.

    Returns:
        created_user: User - created user.
    """
    created_user = random_user_indb(db)
    updated_user = crud_user.set_moderator(db, created_user)
    return updated_user
