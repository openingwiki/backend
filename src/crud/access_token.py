"""
CRUD requests for access token.
"""

from typing import Union

from sqlalchemy import delete
from sqlalchemy.orm import Session

from crud.base import CrudBase
from models import AccessToken, User
from schemas import AccessTokenCreate, AccessTokenUpdate


class CrudAccessToken(CrudBase[AccessToken, AccessTokenCreate, AccessTokenUpdate]):
    def __init__(self, Model: type[AccessToken]):
        super().__init__(Model)

    def get_by_token(self, db: Session, access_token: str) -> Union[AccessToken, None]:
        """
        Getting acces access token row from table by access token.
        If token is expired, None will be returned too.

        Parameters:
            db: Session - database session to deal with.
            access_token: str - access token.

        Returns:
            access_token_model: AccessToken - access token sqlalchemt model.
            None if there isn't such access token.
        """
        return db.query(AccessToken).filter(AccessToken.token == access_token).first()

    def delete_user_tokens(self, db: Session, user: User) -> None:
        """
        Delete all user tokens.

        Parameters:
            db: Session - database session to deal with.
            user: User - user whose passwords to delete.

        Return:
            None
        """
        delete_query = delete(AccessToken).where(AccessToken.user_id == user.id)
        db.execute(delete_query)
        db.commit()