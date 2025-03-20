"""Opening artist SQLAlchemy model."""
import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Table

from database import Base


openings_artists = Table(
    "openings_artists",
    Base.metadata,
    Column("opening_id", Integer, ForeignKey("openings.id"), index=True),
    Column("artist_id", Integer, ForeignKey("artists.id"), index=True),
    Column("created_at", DateTime, default=datetime.datetime.now)
)