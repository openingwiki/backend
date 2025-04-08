import os
import shutil

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from models import Opening
from crud import crud_opening, crud_openings_artists
from core import settings
from schemas import (
    OpeningOut, OpeningCreate, OpeningPost, OpeningPreviewOut
)

from .. import dependencies

router = APIRouter()


@router.get(
    "/",
    description="Get opening by limit and offset.",
    status_code=status.HTTP_200_OK,
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
        openings = crud_opening.search(db, query, limit, offset)

    return [
        OpeningPreviewOut.convert_from_opening(opening) for opening in openings
    ]


@router.post(
    "/",
    description="Add opening.",
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def add_opening(
    opening_post: OpeningPost, db: Session = Depends(dependencies.get_db)
) -> OpeningPreviewOut:
    """Opening create request."""
    opening_create = OpeningCreate.convert_from_opening_post(opening_post=opening_post)
    opening = crud_opening.create(db, opening_create)

    crud_openings_artists.add_openings_artists(db, opening.id, opening_post.artist_ids)

    return OpeningPreviewOut.convert_from_opening(opening)


@router.post(
    "/{opening_id}/preview-image",
    description="Post opening preview image.",
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def add_preview_image(
    opening_id: int, preview: UploadFile = File(...), db: Session = Depends(dependencies.get_db)
):
    """Post opening preview image."""

    if preview.content_type != "image/png" and preview.content_type != "image/jpg":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PNG and JPG images are allowed")

    if not crud_opening.is_opening(db, opening_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opening not found")

    file_path = os.path.join(settings.PATH_TO_THUMBNAILS, str(opening_id))
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(preview.file, buffer)

    return status.HTTP_201_CREATED

@router.get(
    "/{opening_id}",
    description="Get opening.",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True
)
async def get_opening(
    opening_id: int, db: Session = Depends(dependencies.get_db)
) -> OpeningOut:
    opening = crud_opening.get(db, opening_id)

    if not opening:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return OpeningOut.convert_from_opening(opening)