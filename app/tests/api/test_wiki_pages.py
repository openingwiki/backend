"""Tests for /wiki_pages requests."""
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import redis
from app.api import api_router
from app.core import settings
from app.crud import crud_user
from app.db import SessionLocal
from app.tests.utils import clean_db

app = FastAPI()
app.include_router(api_router)
test_client = TestClient(app)


def test_add_wiki_page_to_moderation() -> None:
    """Test case for adding wiki page by usual user."""
    clean_db()
    redis_cache = redis.open_connection()
    redis_cache.flushall()
    user_data = {"email": "forspam@gmail.com", "nickname": "DarkFlameMaster", "password": "password"}
    response = test_client.post(f"/user/register", json=user_data)

    redis_keys = redis_cache.keys()
    email_confirm_token = redis_keys[0]
    response = test_client.get(f"/user/verify", params={"email-confirm-token": email_confirm_token})

    response = test_client.post(f"/user/login", json=user_data)
    response_cookies = response.cookies

    test_client.cookies = response_cookies

    wiki_page_data = {"name": "Bloody Stream", "youtube_url": "https://www.youtube.com/watch?v=PcuTPjgMiXw"}
    response = test_client.post(f"/wiki_pages/add", json=wiki_page_data)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["sended_to_moderation"] == True

    redis_cache.close()


def test_add_wiki_page() -> None:
    """Test case for adding wiki page by moderator."""
    clean_db()
    db = SessionLocal()
    redis_cache = redis.open_connection()
    redis_cache.flushall()
    user_data = {"email": "forspam@gmail.com", "nickname": "DarkFlameMaster", "password": "password"}
    response = test_client.post(f"/user/register", json=user_data)

    redis_keys = redis_cache.keys()
    email_confirm_token = redis_keys[0]
    response = test_client.get(f"/user/verify", params={"email-confirm-token": email_confirm_token})
    user = crud_user.get(db, 1)
    crud_user.set_moderator(db, user)

    response = test_client.post(f"/user/login", json=user_data)
    response_cookies = response.cookies

    test_client.cookies = response_cookies

    wiki_page_data = {"name": "Bloody Stream", "youtube_url": "https://www.youtube.com/watch?v=PcuTPjgMiXw"}
    response = test_client.post(f"/wiki_pages/add", json=wiki_page_data)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["added"] == True

    db.close()
    redis_cache.close()
