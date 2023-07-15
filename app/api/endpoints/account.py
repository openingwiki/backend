from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .. import depenencies
from app import schemas
from app.core import settings, email_sender
from app.crud import crud_account


router = APIRouter()


@router.post("/register")
async def register(db: Session = Depends(depenencies.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """Registering user."""
    email = form_data.username
    password = form_data.password
    account = schemas.AccountIn(
        email=email,
        password=password
    )

    # Adding account to database.
    crud_account.create_account(db, account)
    
    # Sending email.
    email_sender.send_email(
        settings.EMAIL_DOMEN_NAME,
        settings.MAILGUN_API_KEY,
        to=email,
        subject="Registering in opening.wiki",
        text="Your link to activate your acccount:"
    )
