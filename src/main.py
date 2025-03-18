import logging

# Enable SQLAlchemy logging to display all executed queries
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


import models # For database initialization!
from api import app
from core import settings

# Importing and initing database.
from database import SessionLocal
from utils import init_db

with SessionLocal() as db:
    init_db(db)
