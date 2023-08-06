"""Backend can be launched only from here, cause of import errors."""
from app.api import app
from app.db import Base, engine

Base.metadata.create_all(bind=engine)
