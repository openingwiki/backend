"""
API requests with prefix /wiki_pages.
There are function to deal with wiki_pages: add and etc.

API requests quick description:
POST /wiki_pages/add - add wiki_page
"""
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_wiki_page
from app.models import User
from app.schemas import WikiPageCreate

from .. import dependencies

router = APIRouter()


@router.post("/add", description="Request for adding wiki_page.")
async def register(
    wiki_page_data: Annotated[WikiPageCreate, Body()],
    db: Session = Depends(dependencies.get_db),
    user: User = Depends(dependencies.get_current_user),
):
    """
    Adding wiki pages. Geting user access token from cookie.
    If user is moderator, then adding straightaway
    Else request will be sent to moderation.

    Parameters:
        wiki_page_data: Annotated[WikiPageCreate, Body()] - wiki_page data in body with json
        db: Session - SQLAlchemy session to database, initializing in dependency injection.
        user: User - user sqlalchemy model, dependency injection gets access token from cookie then user.

    Returns:
        Muda json.
    """
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    if user.is_moderator:
        wiki_page_data.added_by_user = user.id
        wiki_page_data.needs_moderation = False
        crud_wiki_page.create(db, wiki_page_data)
        return {"added": True}

    else:
        wiki_page_data.added_by_user = user.id
        # Needs moderation field is True by default.
        crud_wiki_page.create(db, wiki_page_data)
        return {"sended_to_moderation": True}