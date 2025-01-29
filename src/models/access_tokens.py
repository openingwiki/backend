"""Access token SQLAlchemy model."""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class AccessToken(Base):
    __tablename__ = "access_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, unique=True)
    token = Column(String, index=True, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

    user = relationship("User", back_populates="access_tokens", uselist=False)