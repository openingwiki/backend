"""Test cases for /user/login requests."""
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import redis
from app.api import api_router
from app.core import settings
from app.tests.utils import clean_db

app = FastAPI()
app.include_router(api_router)
test_client = TestClient(app)


def test_user_login() -> None:
    clean_db()
    redis_cache = redis.open_connection()
    redis_cache.flushall()
    user_data = {"email": "forspam@gmail.com", "nickname": "DarkFlameMaster", "password": "password"}
    response = test_client.post(f"/user/register", json=user_data)

    redis_keys = redis_cache.keys()
    email_confirm_token = redis_keys[0]
    response = test_client.get(f"/user/verify", params={"email-confirm-token": email_confirm_token})

    response = test_client.post(f"/user/login", json=user_data)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["access_token"] == response.cookies.get("access_token")
    assert len(response_json["access_token"]) == settings.TOKEN_LENGHT_IN_BYTES * 2

    redis_cache.close()
