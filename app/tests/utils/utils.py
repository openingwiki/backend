from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DropTable

from app.db import Base, engine


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def clean_db():
    """
    WARNING!!!
    Cleaning database by dropping every table.
    USE ONLY FOR TESTING!!!
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
