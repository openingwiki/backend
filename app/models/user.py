"""User SQLAlchemy model."""
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    verified = Column(Boolean, default=False)
    nickname = Column(String, unique=True, index=True)
    avatar_path = Column(String, default=None)
    is_moderator = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    tokens = relationship("Token", back_populates="user")
    added_wiki_pages = relationship("WikiPages", back_populates="rl_added_by_user")
