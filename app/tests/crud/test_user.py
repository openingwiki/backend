"""User CRUD testing."""
from app.core import security, settings
from app.crud import crud_user
from app.db import SessionLocal
from app.models import User
from app.schemas import UserCreate
from app.tests.utils import clean_db, random_pydantic_user_create

if not settings.IS_SETTINGS_FOR_TEST:
    exit()


def test_create_user() -> None:
    """Test case for inserting user into database."""
    clean_db()
    db = SessionLocal()
    test_user_create_schema: UserCreate = random_pydantic_user_create()

    created_user: User = crud_user.create(db, test_user_create_schema)

    assert created_user.id == 1  # First user id must be equal 1.
    assert created_user.email == test_user_create_schema.email
    assert created_user.nickname == test_user_create_schema.nickname
    assert created_user.hashed_password != "password"
    assert security.verify_password("password", created_user.hashed_password) == True

    db.close()


def test_get_user() -> None:
    """Test case for selecting user from database."""
    clean_db()
    db = SessionLocal()
    test_user_create_schema: UserCreate = random_pydantic_user_create()

    _: User = crud_user.create(db, test_user_create_schema)
    user: User = crud_user.get(db, 1)

    assert user.id == 1
    assert user.email == test_user_create_schema.email
    assert user.nickname == test_user_create_schema.nickname
    assert security.verify_password("password", user.hashed_password) == True

    db.close()
