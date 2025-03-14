from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from sqlalchemy.orm import Session

from crud import CrudAnime
from models import Anime
from schemas import (
    AnimeCreate, AnimeOut
)
from core import settings

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
    anime_name: Annotated[str, Form(alias="name")], anime_preview: UploadFile = File(alias="preview"), db: Session = Depends(dependencies.get_db)
) -> AnimeOut:
    """Request to add anime."""
    if anime_preview.content_type != 'image/png':
        raise HTTPException(status_code=400, detail="File is not a PNG image")

    anime_create = AnimeCreate(name=anime_name)
    anime = crud_anime.create(db, anime_create)

    try:
        target_path = settings.PATH_TO_ANIME_PREVIEWS / f"{anime.id}.png"
        with open(target_path, "wb") as f:
            f.write(await anime_preview.read())
    except:
        print("Error while loading image.")

    return anime