from sqlalchemy.orm import Session

from app.crud import crud_user
from app.models import User
from app.schemas import UserCreate


def random_user_indb(db: Session) -> User:
    """
    Creating random user and inserting it into db.

    Parameters:
        db: Session - database session to deal with.

    Returns:
        created_user: User - created user.
    """
    random_user = UserCreate(email="forspam@gmail.com", nickname="DarkFlameMaster", password="password")
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
    random_user = UserCreate(email="forspam@gmail.com", nickname="DarkFlameMaster", password="password")
    created_user: User = crud_user.create(db, random_user)
    updated_user = crud_user.set_moderator(db, created_user)
    return updated_user


def random_pydantic_user_create() -> UserCreate:
    """
    Random pydantic user create.

    Parameters:
        nothing.

    Returns:
        pydantic_user_create: UserCreate - random pydantic user create model.
    """
    pydantic_user_create = UserCreate(email="forspam@gmail.com", nickname="DarkFlameMaster", password="password")
    return pydantic_user_create
