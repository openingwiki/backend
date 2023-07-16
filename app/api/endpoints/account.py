from sqlalchemy.orm import Session
from redis import Redis
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import HttpUrl
from typing import Annotated

from .. import depenencies
from app import schemas
from app.core import settings, email_sender, security
from app.crud import crud_account, crud_email_confirm_token


router = APIRouter()


@router.post("/register")
async def register(
    db: Session = Depends(depenencies.get_db),
    redis: Redis = Depends(depenencies.get_redis),
    form_data: OAuth2PasswordRequestForm = Depends()
    ):
    """Registering user."""
    email = form_data.username
    password = form_data.password
    account = schemas.AccountIn(
        email=email,
        password=password
    )

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
        text=f"Your link to activate your acccount: {confirmation_link}"
    )

@router.get("/verify")
async def verify(
    *,
    db: Session = Depends(depenencies.get_db),
    redis: Redis = Depends(depenencies.get_redis),
    email_confirm_token: Annotated[str, Query(alias='email-confirm-token')]
    ):
    """"""
    account_id = crud_email_confirm_token.verify_email_confirm_token(redis=redis, token=email_confirm_token)

    # Exception if token doesn't exist.
    if not account_id:
        raise HTTPException(status_code=498, detail="Invalid token")

    account = crud_account.get_account(db, account_id=account_id)
    crud_account.verify_account(db, account)

    return {"account": "verified"}