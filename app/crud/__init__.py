"""CRUD requests for database tables and redis cache."""
from .crud_access_token import CRUDAccessToken
from .crud_email_confirm_token import CRUDEmailConfirmToken
from .crud_user import CRUDUser
from .crud_wiki_page import CrudWikiPage

from app.models import AccessToken, User, WikiPage

crud_user = CRUDUser(User)
crud_access_token = CRUDAccessToken(AccessToken)
crud_wiki_page = CrudWikiPage(WikiPage)
crud_email_confirm_token = CRUDEmailConfirmToken()
