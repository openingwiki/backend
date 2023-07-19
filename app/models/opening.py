"""Token SQLAlchemy model."""
from app.db import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Opening(Base):
    __tablename__ = "openings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    youtube_url = Column(String, unique=True, index=True)
    added_by_user = Column(Integer, ForeignKey("users.id"))
    needs_moderation = Column(Boolean, default=True)

    rl_added_by_user = relationship("User", back_populates="added_openings")
