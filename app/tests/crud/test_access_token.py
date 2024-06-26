"""User CRUD testing."""
from app.core import settings
from app.crud import crud_access_token
from app.db import SessionLocal
from app.models import AccessToken, User
from app.tests.utils import (
    clean_db,
    random_access_token_indb,
    random_pydantic_access_token_create,
    random_user_indb,
)

if not settings.IS_SETTINGS_FOR_TEST:
    exit()


def test_create_access_token() -> None:
    """Test case for access token creation."""
    clean_db()
    db = SessionLocal()
    test_user: User = random_user_indb(db)
    test_access_token_create = random_pydantic_access_token_create(test_user)
    access_token: AccessToken = crud_access_token.create(db, test_access_token_create)

    assert access_token.user_id == test_user.id
    assert len(access_token.token) == settings.TOKEN_LENGHT_IN_BYTES * 2

    db.close()


def test_get_access_token() -> None:
    """Test case for access token getting."""
    clean_db()
    db = SessionLocal()
    test_user: User = random_user_indb(db)
    test_access_token: AccessToken = random_access_token_indb(db, test_user)

    test_access_token: AccessToken = crud_access_token.get_by_access_token(db, test_access_token.token)

    assert test_access_token.token == test_access_token.token
    assert test_access_token.id == test_access_token.id
    assert test_access_token.user_id == test_user.id

    db.close()
