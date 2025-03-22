import os
import shutil

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form, status
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from models import Opening
from crud import crud_opening, crud_openings_artists
from core import settings
from schemas import (
    OpeningOut, OpeningCreate, OpeningPost, OpeningPreviewOut
)

from .. import dependencies

router = APIRouter()


def extract_youtube_id(youtube_embed_link: str) -> str:
    return youtube_embed_link.split("/")[-1]

def generate_opening_out(opening: Opening) -> OpeningOut:
    return OpeningOut(
        id=opening.id,
        name=opening.name,
        anime_id=opening.anime_id,
        artist_ids=[artist.id for artist in opening.artists],
        youtube_embed_link=HttpUrl(opening.youtube_embed_link),
        thumbnail_link=HttpUrl(
            f"https://img.youtube.com/vi/{extract_youtube_id(opening.youtube_embed_link)}/hqdefault.jpg"
        )
    )

def generate_opening_preview_out(opening: Opening) -> OpeningPreviewOut:
    return OpeningPreviewOut(
        id=opening.id,
        name=opening.name,
        thumbnail_link=HttpUrl( f"https://img.youtube.com/vi/{extract_youtube_id(opening.youtube_embed_link)}/hqdefault.jpg")
    )

@router.get(
    "/",
    description="Get opening by limit and offset.",
    status_code=200,
    response_model_exclude_none=True
)
async def search_openings(
    limit: int, offset: int, query: str = "", db: Session = Depends(dependencies.get_db)
) -> list[OpeningPreviewOut]:
    """
    Search openings by limit, offset, and query.
    If empty query is specified, then random openings will be returned.
    """
    openings: list[Opening] = []

    if query == "":
        openings = crud_opening.get_by_limit_and_offset(db, limit, offset)
    else:
        # TODO: search method.
        openings = crud_opening.get_by_limit_and_offset(db, limit, offset)

    return [
        generate_opening_preview_out(opening) for opening in openings
    ]


@router.post(
    "/",
    description="Add opening.",
    status_code=201,
    response_model_exclude_none=True,
)
async def add_opening(
    opening_post: OpeningPost, db: Session = Depends(dependencies.get_db)
) -> OpeningOut:
    """Opening create request."""
    opening_create = OpeningCreate.convert_from_opening_post(opening_post=opening_post)
    opening = crud_opening.create(db, opening_create)

    crud_openings_artists.add_openings_artists(db, opening.id, opening_post.artist_ids)

    return generate_opening_out(opening)


@router.post(
    "/{opening_id}/preview-image",
    description="Post opening preview image.",
    status_code=201,
    response_model_exclude_none=True,
)
async def add_preview_image(
    opening_id: int, preview: UploadFile = File(...), db: Session = Depends(dependencies.get_db)
):
    """Post opening preview image."""

    if preview.content_type != "image/png" and preview.content_type != "image/jpg":
        raise HTTPException(status_code=400, detail="Only PNG and JPG images are allowed")

    if not crud_opening.is_opening(db, opening_id):
        raise HTTPException(status_code=404, detail="Opening not found")

    file_path = os.path.join(settings.PATH_TO_THUMBNAILS, str(opening_id))
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(preview.file, buffer)

    return 201