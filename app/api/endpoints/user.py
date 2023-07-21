"""
API requests with prefix /user.
There are function to deal with user: registering, verifying and etc.

API requests quick description:
POST /user/register - register user
GET /user/verify - verify user
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from redis import Redis
from sqlalchemy.orm import Session

from app import models, schemas
from app.core import email_sender, security, settings
from app.crud import crud_access_token, crud_email_confirm_token, crud_user

from .. import dependencies

router = APIRouter()


@router.post("/register", description="Request for registering user.")
async def register(
    user_data: schemas.UserCreate,
    db: Session = Depends(dependencies.get_db),
    redis: Redis = Depends(dependencies.get_redis),
):
    """
    Registering user.

    Parameters:
        user_data: body of the request with email, password and nickname.
        db: Session - SQLAlchemy session to database, initializing in dependency injection.
        redis: Redis - Redis session for caching, using to store email confirmation token with TTL.

    Returns:
        (for now)Nothing.
    """

    # Adding user to database.
    user = crud_user.create(db, user_data)

    # Creating access token to email confirmation.
    email_confirm_token = crud_email_confirm_token.create(redis, user)
    confirmation_link = f"http://{settings.API_DOMAIN}/user/verify?email-confirm-token={email_confirm_token}"

    # Sending email.
    email_sender.send_email(
        settings.EMAIL_DOMEN_NAME,
        settings.MAILGUN_API_KEY,
        to=user.email,
        subject="Registering in opening.wiki",
        text=f"Your link to activate your acccount: {confirmation_link}",
    )

    return {"message": "user has been registered"}


@router.get("/verify", description="Request for email verification.")
async def verify(
    *,
    db: Session = Depends(dependencies.get_db),
    redis: Redis = Depends(dependencies.get_redis),
    email_confirm_token: Annotated[str, Query(alias="email-confirm-token")],
    response: Response,
):
    """
    Verifying email.

    Parameters:
        db: Session - SQLAlchemy session to database, initializing in dependency injection.
        redis: Redis - Redis session for caching, using to store email confirmation token with TTL.
        email_confirm_token: Annotated[str, Query(alias="email-confirm-token")] - query parameter with token string,
            query parameter name must be 'email-confirm-token'.

    Returns:
        JSON with access token info.
        HTTPException 401 - Invalid token. Token also might be expired.
    """
    user_id = crud_email_confirm_token.verify(redis, email_confirm_token)

    # Exception if email confirmation token doesn't exist.
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid email confirmation token")

    user = crud_user.get(db, user_id=user_id)
    crud_user.verify(db, user)

    access_token = models.AccessToken(token=security.create_token(), user_id=user.id)
    access_token: models.AccessToken = crud_access_token.create(db, access_token)
    response.set_cookie("access_token", access_token.token)
    return {"access_token": access_token.token}


@router.post("/login", description="Request for login.")
async def login(*, response: Response, db: Session = Depends(dependencies.get_db), user_data: schemas.UserLogin):
    """
    Authorizing.

    Parameters:
        db: Session - SQLAlchemy session to database, initializing in dependency injection.
        form_data: OAuth2 standard form for user data, must contain username and password.

    Returns:
        JSON with access token info.
        HTTPException 401 - Invalid credentials.
    """
    email = user_data.email
    password = user_data.password
    user: models.User = crud_user.get_by_email(db, email)
    if not user:  # Exception if there isn't such email.
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.verified:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, deatil="Email not verified")

    is_password_correct = security.verify_password(password, user.hashed_password)
    if not is_password_correct:  # Exception if password doesn't match with password hash.
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = models.AccessToken(token=security.create_token(), user_id=user.id)
    access_token: models.AccessToken = crud_access_token.create(db, access_token)
    response.set_cookie("access_token", access_token.token)
    return {"access_token": access_token.token}
