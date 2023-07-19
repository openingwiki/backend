"""
API requests with prefix /user.
There are function to deal with user: registering, verifying and etc.

API requests quick description:
POST /user/register - register user
GET /user/verify - verify user
"""
from sqlalchemy.orm import Session
from redis import Redis
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel, HttpUrl

from .. import dependencies
from app import schemas
from app.core import settings, email_sender, security
from app.crud import crud_email_confirm_token, crud_token, crud_user, crud_opening
from app import models


router = APIRouter()


@router.post("/add", description="Request for adding opening.")
async def register(
    opening_data: Annotated[schemas.OpeningAdd, Body()],
    db: Session = Depends(dependencies.get_db),
    redis: Redis = Depends(dependencies.get_redis),
    user: models.User = Depends(dependencies.get_current_user),
):
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
    
