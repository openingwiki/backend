"""Artist SQLAlchemy model."""
import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base
from models.opening_artist import OpeningArtist


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)

    openings = relationship("Opening", secondary=OpeningArtist, back_populates="artists")