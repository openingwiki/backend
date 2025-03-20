import os
import shutil

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form, status
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from crud import crud_opening, crud_openings_artists
from core import settings
from schemas import (
    OpeningOut, OpeningCreate, OpeningUpdate, OpeningPost
)

from .. import dependencies

router = APIRouter()



@router.post(
    "/",
    description="Add opening.",
    status_code=201,
    response_model_exclude_none=True,
)
async def add_opening(
    opening_post: OpeningPost, db: Session = Depends(dependencies.get_db)
):
    """Opening create request."""
    opening_create = OpeningCreate.convert_from_opening_post(opening_post=opening_post)
    opening = crud_opening.create(db, opening_create)

    crud_openings_artists.add_openings_artists(db, opening.id, opening_post.artist_ids)

    return status.HTTP_201_CREATED


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
