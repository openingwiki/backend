"""Opening SQLAlchemy model."""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from models.opening_artist import openings_artists


class Opening(Base):
    __tablename__ = "openings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    anime_id = Column(Integer, ForeignKey("anime.id"), index=True)
    youtube_embed_link = Column(String)
    thumbnail_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

    anime = relationship("Anime", back_populates="openings", uselist=False)
    artists = relationship("Artist", secondary=openings_artists, back_populates="openings")