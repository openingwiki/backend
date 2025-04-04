from typing import Annotated

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from crud import crud_artist
from schemas import (
    ArtistCreate, ArtistOut, ArtistPost
)

from .. import dependencies

router = APIRouter()

@router.post(
    "/",
    description="Add artist.",
    status_code=201,
    response_model_exclude_none=True,
)
async def add_artist(
    artist_post: ArtistPost, db: Session = Depends(dependencies.get_db)
) -> ArtistOut:
    """Request to add artist."""
    artist_create = ArtistCreate.convert_from_artist_post(artist_post)
    artist = crud_artist.create(db, artist_create)
    return artist


@router.get(
    "/",
    description="Find artist by query.",
    status_code=200,
    response_model_exclude_none=True,
)
async def find_artist(
    query: str, db: Session = Depends(dependencies.get_db)
) -> list[ArtistOut]:
    """Search for artist by name."""
    artist_list = []
    if query != "":
        artist_list = crud_artist.search_by_name(db, query)
    else:
        artist_list = crud_artist.get_by_limit(db)

    return artist_list