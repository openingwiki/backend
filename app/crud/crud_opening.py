"""
"""
from sqlalchemy.orm import Session
from typing import Union

from app import models
from app import schemas
from app.core import security


def add_opening(db: Session, opening: schemas.OpeningAdd, needs_moderation: bool = True) -> models.User:
    """ """
    opening_model = models.Opening(
        name=opening.name, youtube_url=opening.youtube_url, added_by_user=opening.added_by_user, needs_moderation=needs_moderation
    )
    db.add(opening_model)
    db.commit()
    db.refresh(opening_model)
    return opening_model
