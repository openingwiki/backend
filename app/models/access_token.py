"""Access token SQLAlchemy model."""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class AccessToken(Base):
    __tablename__ = "access_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, index=True, unique=True)

    user = relationship("User", back_populates="access_tokens")
