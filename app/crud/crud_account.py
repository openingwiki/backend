from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.core import security


def create_account(db: Session, account: schemas.AccountIn):
    account_hashed_password = security.get_password_hash(account.password)
    account_model = models.Account(
        email=account.email,
        hashed_password=account_hashed_password,
        verified = False
    )
    db.add(account_model)
    db.commit()
    db.refresh(account_model)

def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.account_id == account_id).first()
