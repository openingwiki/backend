"""Account SQLAlchemy model."""
from app.db import Base

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    verified = Column(Boolean, default=False)

    tokens = relationship("Token", back_populates="account")