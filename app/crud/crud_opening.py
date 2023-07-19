"""
CRUD requests for openings.
"""
from typing import Union

from sqlalchemy.orm import Session

from app import models, schemas


def add_opening(db: Session, opening: schemas.OpeningAdd, needs_moderation: bool = True) -> models.Opening:
    """
    Adding opening into database.

    Parameters:
        db: Session - db session to deal with.
        opening: schemas.OpeningAdd - pydantic model for requests with opening.
        needs_moderation: bool - flag that opening needs to be moderated.

    Returns:
        models.Opening - added opening sqlalchemy model.
    """
    opening_model = models.Opening(
        name=opening.name,
        youtube_url=opening.youtube_url,
        added_by_user=opening.added_by_user,
        needs_moderation=needs_moderation,
    )
    db.add(opening_model)
    db.commit()
    db.refresh(opening_model)
    return opening_model
