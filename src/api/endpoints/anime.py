from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from crud import CrudAnime
from models import Anime
from schemas import (
    AnimeCreate, AnimeOut, AnimePost
)
from core import settings

from .. import dependencies

router = APIRouter()

crud_anime = CrudAnime(Anime)


@router.post(
    "/",
    description="Add anime.",
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def add_anime(
    anime_post: AnimePost, db: Session = Depends(dependencies.get_db)
) -> AnimeOut:
    """Request to add anime."""
    anime_create = AnimeCreate.convert_from_anime_post(anime_post)
    anime = crud_anime.create(db, anime_create)
    return anime


@router.post(
    "/{anime_id}/preview-image",
    description="Add anime preview.",
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True
)
async def add_anime_preview_image(
    anime_id: int,  anime_preview: UploadFile = File(alias="preview"), db: Session = Depends(dependencies.get_db)
):
    """Request to add anime preview image."""
    if anime_preview.content_type != 'image/png':
        raise HTTPException(status_code=400, detail="File is not a PNG image")

    if not crud_anime.is_anime(db, anime_id):
       raise HTTPException(status_code=404, detail="Opening not found")

    try:
        target_path = settings.PATH_TO_ANIME_PREVIEWS / f"{anime_id}.png"
        with open(target_path, "wb") as f:
            f.write(await anime_preview.read())
    except:
        print("Error while loading image.")

    return status.HTTP_201_CREATED


@router.get(
    "/",
    description="Find anime by query.",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def find_anime(
    query: str, db: Session = Depends(dependencies.get_db)
) -> list[AnimeOut]:
    """Search for anime by name."""
    anime_list = []
    if query != "":
        anime_list = crud_anime.search_by_name(db, query)
    else:
        anime_list = crud_anime.get_by_limit(db)
    return anime_list