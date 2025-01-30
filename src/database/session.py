"""
Creating database engine and such things.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from core import settings


engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db(db: Session):
    if settings.DROP_DATABASE_EVERY_LAUNCH:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)