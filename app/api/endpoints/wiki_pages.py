"""
API requests with prefix /wiki_pages.
There are function to deal with wiki_pages: add and etc.

API requests quick description:
POST /wiki_pages/add - add wiki_page
"""
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import crud_wiki_page
from app.models import User, WikiPage
from app.schemas import WikiPageCreate, WikiPageOut

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
    if user.is_moderator:
        wiki_page_data.added_by_user = user.id
        wiki_page_data.needs_moderation = False
        crud_wiki_page.create(db, wiki_page_data)
        return {"added": True, "sended_to_moderation": True}

    else:
        wiki_page_data.added_by_user = user.id
        # Needs moderation field is True by default.
        crud_wiki_page.create(db, wiki_page_data)
        return {"added": True, "sended_to_moderation": True}


@router.get(
    "/last_added_wiki_pages", description="Request for getting last added wiki pages.", response_model=list[WikiPageOut]
)
async def get_last_added_wiki_pages(
    limit: Annotated[int, Query(gt=0, le=100)],
    db: Session = Depends(dependencies.get_db),
    user: User = Depends(dependencies.get_current_user),
):
    """
    Getting last added wiki pages.

    Parameters:
        limit: Annotated[int, Query(gt=0, le=100)] - count of last added wiki pags, must be > 0 and <= 100.
        db: Session - SQLAlchemy session to database, initializing in dependency injection.
        user: User - user sqlalchemy model, dependency injection gets access token from cookie then user.

    Returns:
        Muda json.
    """
    last_added_wiki_pages: list[WikiPage] = crud_wiki_page.get_last_added(db, limit=limit)
    return last_added_wiki_pages
