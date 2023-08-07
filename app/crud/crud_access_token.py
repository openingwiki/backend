"""
CRUD requests for access token.
"""
from typing import Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import AccessToken
from app.schemas import AccessTokenCreate


class CRUDAccessToken(CRUDBase[AccessToken, AccessTokenCreate]):
    def __init__(self, Model: type[AccessToken]):
        super().__init__(Model)

    def get_by_access_token(self, db: Session, access_token: str) -> Union[AccessToken, None]:
        """
        Getting acces access token row from table by access token.

        Parameters:
            db: Session - database session to deal with.
            access_token: str - access token.

        Returns:
            access_token_model: AccessToken - access token sqlalchemt model.
            None if there isn't such access token.
        """
        return db.query(AccessToken).filter(AccessToken.token == access_token).first()
