from app.crud import crud_access_token
from app.models import User, AccessToken


def random_access_token_indb(db, user: User) -> AccessToken:
    created_access_token: AccessToken = crud_access_token.create(db, user)
    return created_access_token



