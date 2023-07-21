"""Backend can be launched only from here, cause of import errors."""
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

from app.api import app
