from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import CrudAnime
from models import Anime
from schemas import (
    AnimeCreate, AnimeOut
)

from .. import dependencies

router = APIRouter()

crud_anime = CrudAnime(Anime)


@router.post(
    "/",
    description="Add anime.",
    status_code=201,
    response_model_exclude_none=True,
)
async def add_anime(
    anime_create: AnimeCreate, db: Session = Depends(dependencies.get_db)
) -> AnimeOut:
    """Request to add anime."""
    anime = crud_anime.create(db, anime_create)
    return anime