"""Opening artist SQLAlchemy model."""
import datetime
from sqlalchemy import Column, Integer, DateTime

from database import Base


class OpeningArtist(Base):
    __tablename__ = "opening_artists"

    id = Column(Integer, primary_key=True, index=True)
    opening_id = Column(Integer, index=True)
    artist_id = Column(Integer, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
