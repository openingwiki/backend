"""WikiPage SQLAlchemy model."""
import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class WikiPage(Base):
    __tablename__ = "wiki_pages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    youtube_url = Column(String, unique=True, index=True)
    added_by_user = Column(Integer, ForeignKey("users.id"))
    needs_moderation = Column(Boolean, default=True)
    added_at = Column(DateTime, default=datetime.datetime.utcnow)

    rl_added_by_user = relationship("User", back_populates="added_wiki_pages")
