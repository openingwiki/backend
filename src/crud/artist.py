"""
CRUD requests for the artist.
"""

from sqlalchemy.orm import Session

from crud.base import CrudBase
from models import Artist
from schemas import ArtistCreate, ArtistOut, ArtistUpdate


class CrudArtist(CrudBase[Artist, ArtistCreate, ArtistUpdate]):
    def __init__(self, Model: type[Artist]):
        super().__init__(Model)

    def search_by_name(self, db: Session, query: str, limit: int = 10) -> list[Artist]:
        """Search for artist by name with a limit of results."""
        return (
            db.query(Artist)
            .filter(Artist.name.ilike(f"%{query}%"))
            .limit(limit)
            .all()
        )