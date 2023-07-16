from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.core import security


def create_token(db: Session, Account: schemas.AccountInDB, token: schemas.TokeIn):
    token_model = models.Token(
        account_id=Account.account_id,
        token=token.token
    )
    db.add(token_model)
    db.commit()
    db.refresh(token_model)

def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.account_id == account_id).first()
