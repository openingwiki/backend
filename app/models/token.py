"""Token SQLAlchemy model."""
from app.db import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Token(Base):
    __tablename__ = "tokens"

    token_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"))
    token = Column(String, index=True)

    account = relationship("Account", back_populates="tokens")