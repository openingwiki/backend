from app.crud import crud_access_token
from app.models import User, Token


def random_token_indb(db, user: User) -> Token:
    created_token: Token = crud_access_token.create(db, user)
    return created_token



