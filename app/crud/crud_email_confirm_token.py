from typing import Union
from redis import Redis

from app import schemas
from app.core import security


def create_email_confirm_token(redis: Redis, account: schemas.AccountInDB) -> str:
    token = security.create_access_token(token_lenght=64)
    redis.set(token, account.account_id, ex=3600*3) # Exires after 3 hours.
    return token

def verify_email_confirm_token(redis: Redis, token: str) -> Union[int, None]:
    value = redis.get(token)
    if value:
        redis.delete(token)
    return value
