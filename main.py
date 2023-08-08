"""Backend can be launched only from here, cause of import errors."""
# Importing API routers.
from fastapi import FastAPI

from app.api import api_router
from app.core import settings

app = FastAPI()
app.include_router(api_router, prefix=settings.API_REQUEST_PREFIX)


# Importing and initing database.
from app.db import SessionLocal
from app.db.init_db import init_db

db = SessionLocal()
init_db(db)
db.close()
