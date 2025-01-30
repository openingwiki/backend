import os
import shutil
from io import BytesIO

from PIL import Image
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from crud import CrudOpening
from core import settings
from models import Opening, User
from schemas import (
    OpeningPost, OpeningOut, OpeningCreate, OpeningUpdate
)

from .. import dependencies

router = APIRouter()

crud_opening = CrudOpening(Opening)


@router.post(
    "/",
    description="Add opening.",
    status_code=201,
    response_model_exclude_none=True,
)
async def add_opening(
    name: str = Form(...), anime_id: int = Form(...), youtube_embed_link: HttpUrl = Form(...), thumbnail: UploadFile = File(...), db: Session = Depends(dependencies.get_db), user: User = Depends(dependencies.get_current_user)
) -> OpeningOut:
    """Opening create request."""
    opening_create = OpeningCreate(name=name, anime_id=anime_id, youtube_embed_link=str(youtube_embed_link))
    opening = crud_opening.create(db, opening_create)

    if thumbnail.content_type != "image/png" and thumbnail.content_type != "image/jpg":
        raise HTTPException(status_code=400, detail="Only PNG and JPG images are allowed")

    contents = await thumbnail.read()

    try:
        # Verify it's a PNG image
        image = Image.open(BytesIO(contents))
        if image.format != "PNG" and image.format != "JPG":
            raise HTTPException(status_code=400, detail="Invalid PNG or JPG file")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid PNG or JPG file")

    # Reset file pointer (since we read it)
    thumbnail.file.seek(0)

    file_path = os.path.join(settings.PATH_TO_THUMBNAILS, str(opening.id))
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(thumbnail.file, buffer)
    
    opening = crud_opening.update(db, opening, OpeningUpdate(thumbnail_path=file_path))
    return opening