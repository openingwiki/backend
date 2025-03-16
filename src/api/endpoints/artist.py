from typing import Annotated

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from crud import crud_artist
from schemas import (
    ArtistCreate, ArtistOut
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
    artist_name: Annotated[str, Form(alias="name")], db: Session = Depends(dependencies.get_db)
) -> ArtistOut:
    """Request to add anime."""
    artist_create = ArtistCreate(name=artist_name)
    artist = crud_artist.create(db, artist_create)
    return artist