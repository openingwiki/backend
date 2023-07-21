from fastapi.testclient import TestClient

from app.api import app
from app.core.config import settings
from app.redis import open_connection
from app.tests.utils import clean_db

test_client = TestClient(app)


def test_user_register() -> None:
    clean_db()
    user_data = {"email": "forspam@gmail.com", "nickname": "DarkFlameMaster", "password": "password"}
    response = test_client.post(f"/user/register", json=user_data)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["message"] == "user has been registered"


def test_user_verify() -> None:
    clean_db()
    redis = open_connection()
    redis.flushall()

    user_data = {"email": "forspam@gmail.com", "nickname": "DarkFlameMaster", "password": "password"}
    response = test_client.post(f"/user/register", json=user_data)

    redis_keys = redis.keys()
    email_confirm_token = redis_keys[0]

    assert email_confirm_token != None

    response = test_client.get(f"/user/verify", params={"email-confirm-token": email_confirm_token})
    response_json = response.json()
    assert response.status_code == 200
    assert len(response.cookies.get("access_token")) == settings.TOKEN_LENGHT_IN_BYTES * 2
    assert len(response_json["access_token"]) == settings.TOKEN_LENGHT_IN_BYTES * 2
    assert response_json["access_token"] == response.cookies.get("access_token")

    redis.close()
