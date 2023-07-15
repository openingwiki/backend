from app.db import Base

from sqlalchemy import Column, Integer, String, Boolean


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    verified = Column(Boolean, default=False)