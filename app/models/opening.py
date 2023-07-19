"""Opening SQLAlchemy model."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Opening(Base):
    __tablename__ = "openings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    youtube_url = Column(String, unique=True, index=True)
    added_by_user = Column(Integer, ForeignKey("users.id"))
    needs_moderation = Column(Boolean, default=True)

    rl_added_by_user = relationship("User", back_populates="added_openings")
