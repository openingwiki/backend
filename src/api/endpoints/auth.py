from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core import security
from crud import CrudAccessToken, CrudUser
from models import AccessToken, User
from schemas import (
    AccessTokenOut,
    UserAuth,
    UserCreate,
    UserOut,
    UserRegistration,
)
from utils import create_token

from .. import dependencies

router = APIRouter()

crud_user = CrudUser(User)
crud_access_token = CrudAccessToken(AccessToken)


@router.post(
    "/register",
    description="Register user.",
    status_code=201,
    response_model_exclude_none=True,
)
async def register_user(
    user_registration: UserRegistration, db: Session = Depends(dependencies.get_db)
) -> AccessTokenOut:
    """
    User registration.

    Status codes:
    201 - success
    409 - already existing username
    """
    if crud_user.is_username(db, user_registration.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="username already exists"
        )

    user_create = UserCreate.convert_from_user_registration(user_registration)
    user = crud_user.create(db, user_create)

    return create_token(db, user)


@router.post("/login", description="Authorization request.", status_code=200)
async def authenticate_user(
    user_auth: UserAuth, db: Session = Depends(dependencies.get_db)
) -> AccessTokenOut:
    """
    Authenticate user by username and password.
    Returning token as response.

    Response codes:
        200 - success
        401 - wrong credentials
    """
    user: User = crud_user.get_by_username(db, user_auth.username)

    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Wrong password or username"
        )

    is_password_correct = security.verify_password(
        user_auth.password, user.hashed_password
    )

    if not is_password_correct:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Wrong password or login"
        )

    return create_token(db, user)