"""
CRUD requests for account.
"""
from sqlalchemy.orm import Session
from typing import Union

from app import models
from app import schemas
from app.core import security


def create_account(db: Session, account: schemas.AccountIn) -> models.Account:
    """
    Adding account into table.

    Parameters:
        db: Session - db session to deal with.
        account: AccountIn - account pydantic model.

    Returns:
        account_model: AccountInDB - SQLAlchemy model with account data.
    """
    account_hashed_password = security.get_password_hash(account.password)
    account_model = models.Account(email=account.email, hashed_password=account_hashed_password, verified=False)
    db.add(account_model)
    db.commit()
    db.refresh(account_model)
    return account_model


def get_account(db: Session, account_id: int) -> Union[models.Account, None]:
    """
    Getting account from table by account id.

    Parameters:
        db: Session - db session to deal with.
        account_id: int - account id of account to get.

    Returns:
        account: Account - SQLAlchemy model with account data.
        None - if there isn't such account.
    """
    return db.query(models.Account).filter(models.Account.account_id == account_id).first()


def get_account_by_email(db: Session, email: str) -> Union[models.Account, None]:
    """
    Getting account from table by email.

    Parameters:
        db: Session - db session to deal with.
        email: int - email of account ot get.

    Returns:
        account: Account - SQLAlchemt model with account data.
        None - if there isn't such account.
    """
    return db.query(models.Account).filter(models.Account.email == email).first()


def verify_account(db: Session, account: models.Account):
    """
    Setting account verified flag to True.

    Parameters:
        db: Session - db session to deal with.
        account - account SQLAlchemy model.

    Returns
        Nothing
    """
    account.verified = True
    db.commit()
