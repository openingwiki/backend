"""
CRUD requests for account.
"""
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.core import security


def create_account(db: Session, account: schemas.AccountIn) -> schemas.AccountInDB:
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


def get_account(db: Session, account_id: int) -> models.Account:
    """
    Getting account from table.

    Parameters:
        db: Session - db session to deal with.
        account_id: int - account id of account to get.
    
    Returns:
        account: Account - SQLAlchemy model with account data.
    """
    return db.query(models.Account).filter(models.Account.account_id == account_id).first()


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
