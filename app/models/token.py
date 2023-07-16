from app.db import Base

from sqlalchemy import Column, Integer, String


class Token(Base):
    __tablename__ = "tokens"

    token_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer)
    token = Column(String, index=True)