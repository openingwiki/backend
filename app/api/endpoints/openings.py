"""
API requests with prefix /openings.
There are function to deal with openings: add and etc.

API requests quick description:
POST /openings/add - add opening
"""
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import crud_opening

from .. import dependencies

router = APIRouter()


@router.post("/add", description="Request for adding opening.")
async def register(
    opening_data: Annotated[schemas.OpeningAdd, Body()],
    db: Session = Depends(dependencies.get_db),
    user: models.User = Depends(dependencies.get_current_user),
):
    """
    Adding openings. Geting user token from cookie.
    If user is moderator, then adding straightaway
    Else request will be sent to moderation.

    Parameters:
        opening_data: Annotated[schemas.OpeningAdd, Body()] - opening data in body with json
        db: Session - SQLAlchemy session to database, initializing in dependency injection.
        user: models.User - user sqlalchemy model, dependency injection gets token from cookie then user.

    Returns:
        Muda json.
    """
    if not user:
        raise HTTPException(401, "Invalid credentials")

    if user.is_moderator:
        opening_data.added_by_user = user.id
        crud_opening.add_opening(db, opening_data, needs_moderation=False)
        return {"added": True}

    else:
        opening_data.added_by_user = user.id
        crud_opening.add_opening(db, opening_data, needs_moderation=True)
        return {"sended to moderation": True}
