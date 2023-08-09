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


@router.post("/add", description="Request for adding wiki page.")
async def register(
    wiki_page_data: Annotated[WikiPageCreate, Body()],
    db: Session = Depends(dependencies.get_db),
    user: User = Depends(dependencies.get_current_user),
):
    """
    Adding wiki page. Geting user access token from cookie.
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
        wiki_page_data.is_moderated = True
        crud_wiki_page.create(db, wiki_page_data)
        return {"added": True, "sended_to_moderation": True}

    else:
        wiki_page_data.added_by_user = user.id
        # Moderated field is False by default.
        crud_wiki_page.create(db, wiki_page_data)
        return {"added": True, "sended_to_moderation": True}


@router.get("/get/{id}", description="Request for getting one wiki page info.", response_model=WikiPageOut)
async def get(
    id: int,
    db: Session = Depends(dependencies.get_db),
    user: User = Depends(dependencies.get_current_user),
):
    """
    Getting wiki page info by id.

    Parameters:
        id: Annotated[int, Query(gt=0)] - id of wiki page, must be greater than 0.
        db: Session - SQLAlchemy session to database, initializing in dependency injection.
        user: User - user sqlalchemy model, dependency injection gets access token from cookie then user.

    Returns:
        response_model = WikiPageOut
        wiki_page: WikiPage - wiki page info.
    """
    wiki_page = crud_wiki_page.get(db, id=id)

    if not wiki_page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wiki page not found.")

    return wiki_page


@router.get("/last_added", description="Request for getting last added wiki pages.", response_model=list[WikiPageOut])
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
        response_model = list[WikiPageOut]
        last_added_wiki_pages: list[WikiPage] - last added wiki pages.
    """
    last_added_wiki_pages: list[WikiPage] = crud_wiki_page.get_last_added(db, limit=limit)
    return last_added_wiki_pages


@router.get(path="/unmoderated_wiki_pages", description="Getting unmoderated wiki_pages.")
def get_unmoderated_wiki_pages(
    limit: Annotated[int, Query(int, gt=0, le=20)],
    db: Session = Depends(dependencies.get_db),
    moderator: User = Depends(dependencies.get_current_moderator),
):
    """
    Getting umoderated wiki pages, which were sended by usual users.

    Parameters:
        limit: Annotated[int, Query(gt=0, le=100)] - count of unmoderated wiki pags to get, must be > 0 and <= 100.
        db: Session - SQLAlchemy session to database, initializing in dependency injection.
        user: User - user sqlalchemy model, dependency injection gets access token from cookie then user.

    Returns:
        response_model = list[WikiPageOut]
        unmoderated_wiki_pages: list[WikiPage] - unmoderated wiki pages.
    """
    unmoderated_wiki_pages: list[WikiPage] = crud_wiki_page.get_unmoderated(db, limit=limit)
    return unmoderated_wiki_pages


@router.put(path="/approve_addition/{id}", description="Approving addition request for wiki page.")
def approve_wiki_page_addition(
    id: int, db: Session = Depends(dependencies.get_db), moderator: User = Depends(dependencies.get_current_moderator)
):
    """
    Setting unmoderated wiki page to moderated.

    Parameters:
        id: int - id of wiki page to update.
        db: Session - SQLAlchemy session to database, initializing in dependency injection.
        user: User - user sqlalchemy model, dependency injection gets access token from cookie then user.

    Returns:
        Muda JSON.
    """
    wiki_page_to_moderate = crud_wiki_page.get(db, id)

    if not wiki_page_to_moderate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    crud_wiki_page.set_moderated(db, wiki_page_to_moderate)
    return {"message": "ok"}
