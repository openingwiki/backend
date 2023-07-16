"""
API requests with prefix /account.
There are function to deal with account: registering, verifying and etc.

API requests quick description:
POST /account/register - register account
GET /account/verify - verify account
"""
from sqlalchemy.orm import Session
from redis import Redis
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from .. import dependencies
from app import schemas
from app.core import settings, email_sender, security
from app.crud import crud_account, crud_email_confirm_token, crud_token
from app import models


router = APIRouter()


@router.post("/register", description="Request for registering user.")
async def register(
    db: Session = Depends(dependencies.get_db),
    redis: Redis = Depends(dependencies.get_redis),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> None:
    """
    Registering account.

    Parameters:
        db: Session - SQLAlchemy session to database, initializing in dependency injection.
        redis: Redis - Redis session for caching, using to store email confirmation token with TTL.
        form_data: OAuth2 standard form for account data, must contain username and password.

    Returns:
        (for now)Nothing.
    """
    email = form_data.username
    password = form_data.password
    account = schemas.AccountIn(email=email, password=password)

    # Adding account to database.
    account = crud_account.create_account(db, account)

    # Creating token to email confirmation.
    email_confirm_token = crud_email_confirm_token.create_email_confirm_token(redis, account)
    confirmation_link = f"http://{settings.API_DOMAIN}/account/verify?email-confirm-token={email_confirm_token}"

    # Sending email.
    email_sender.send_email(
        settings.EMAIL_DOMEN_NAME,
        settings.MAILGUN_API_KEY,
        to=email,
        subject="Registering in opening.wiki",
        text=f"Your link to activate your acccount: {confirmation_link}",
    )


@router.get("/verify", description="Request for email verification.")
async def verify(
    *,
    db: Session = Depends(dependencies.get_db),
    redis: Redis = Depends(dependencies.get_redis),
    email_confirm_token: Annotated[str, Query(alias="email-confirm-token")],
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
        HTTPException 498 - Invalid token. Token also might be expired.
    """
    account_id = crud_email_confirm_token.verify_email_confirm_token(redis, email_confirm_token)

    # Exception if token doesn't exist.
    if not account_id:
        raise HTTPException(status_code=498, detail="Invalid token")

    account = crud_account.get_account(db, account_id=account_id)
    crud_account.verify_account(db, account)

    token: models.Token = crud_token.create_access_token(db, account)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", description="Request for login.")
async def login(db: Session = Depends(dependencies.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authorizing.

    Parameters:
        db: Session - SQLAlchemy session to database, initializing in dependency injection.
        form_data: OAuth2 standard form for account data, must contain username and password.

    Returns:
        JSON with access token info.
        HTTPException 401 - Invalid credentials.
    """
    email = form_data.username
    password = form_data.password
    account: models.Account = crud_account.get_account_by_email(db, email)
    if not account:  # Exception if there isn't such email.
        raise HTTPException(401, detail="Invalid credentials")

    is_password_correct = security.verify_password(password, account.hashed_password)
    if not is_password_correct:  # Exception if password doesn't match with password hash.
        raise HTTPException(401, detail="Invalid credentials")

    token: models.Token = crud_token.create_access_token(db, account)
    return {"access_token": token, "token_type": "bearer"}
