"""
CRUD requests for token.
"""
from sqlalchemy.orm import Session

from app import models
from app.core import security


def create_access_token(db: Session, account: models.Account) -> str:
    """
    Creating access token.

    Parameters:
        db: Session - database session to deal with.
        account: models.Account - pydantic model of account for which the token is being created.

    Returns:
        token: str - created token.
    """
    token = security.create_access_token()
    token_model = models.Token(token=token, account_id=account.account_id)
    db.add(token_model)
    db.commit()
    db.refresh(token_model)
    return token_model.token
