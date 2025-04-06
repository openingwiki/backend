from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from core import security, settings
from crud import CrudAccessToken, CrudUser
from models import AccessToken, User
from schemas import (
    UserOut,
    UserAuth,
    UserCreate,
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
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def register_user(
    user_registration: UserRegistration, response: Response, db: Session = Depends(dependencies.get_db)
) -> UserOut:
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

    access_token = create_token(db, user)
    response.set_cookie(
        key="access_token", value=access_token.token, 
        samesite="Lax", secure=settings.IS_HTTPS,
        max_age=settings.ACCESS_TOKEN_MAX_AGE
    )
    return access_token.user


@router.post("/login", description="Authorization request.", status_code=status.HTTP_200_OK)
async def authenticate_user(
    user_auth: UserAuth, response: Response, db: Session = Depends(dependencies.get_db)
) -> UserOut:
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

    access_token = create_token(db, user)
    response.set_cookie(
        key="access_token", value=access_token.token, 
        samesite="Lax", secure=settings.IS_HTTPS,
        max_age=settings.ACCESS_TOKEN_MAX_AGE
    )
    return access_token.user