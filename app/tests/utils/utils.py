from app.db import Base, engine


def clean_db():
    """
    WARNING!!!
    Cleaning database by dropping every table.
    USE ONLY FOR TESTING!!!
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
