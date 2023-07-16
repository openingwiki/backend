from typing import Generator

from app.db import SessionLocal
from app.redis import open_connection


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_redis() -> Generator:
    try:
        redis = open_connection()
        yield redis
    finally:
        redis.close()