"""
WikiPage CRUD testing.
Tests must be launched in declared order to check every function properly.
"""
from app.core import settings
from app.crud import crud_wiki_page
from app.db import SessionLocal
from app.models import WikiPage
from app.schemas import UserCreate
from app.tests.utils import (
    clean_db,
    random_moderator_indb,
    random_pydantic_wiki_page,
    random_user_indb,
)

if not settings.IS_SETTINGS_FOR_TEST:
    exit()


def test_moderator_create_wiki_page():
    """Test case for wiki page creation with moderator."""
    clean_db()
    db = SessionLocal()
    test_user = random_moderator_indb(db)
    test_wiki_page = random_pydantic_wiki_page(test_user)

    needs_moderation = not test_user.is_moderator
    created_wiki_page: WikiPage = crud_wiki_page.create(db, test_wiki_page, needs_moderation=needs_moderation)

    assert created_wiki_page.name == test_wiki_page.name
    assert created_wiki_page.youtube_url == test_wiki_page.youtube_url
    assert created_wiki_page.added_by_user == test_user.id
    assert created_wiki_page.needs_moderation == False

    db.close()


def test_user_create_wiki_page():
    """Test case for wiki page creation with usual user."""
    clean_db()
    db = SessionLocal()
    test_user = random_user_indb(db)
    test_wiki_page = random_pydantic_wiki_page(test_user)

    needs_moderation = not test_user.is_moderator
    created_wiki_page: WikiPage = crud_wiki_page.create(db, test_wiki_page, needs_moderation=needs_moderation)

    assert created_wiki_page.name == test_wiki_page.name
    assert created_wiki_page.youtube_url == test_wiki_page.youtube_url
    assert created_wiki_page.added_by_user == test_user.id
    assert created_wiki_page.needs_moderation == True

    db.close()
