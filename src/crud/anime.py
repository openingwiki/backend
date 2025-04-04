"""
CRUD requests for the anime.
"""

from sqlalchemy.orm import Session

from crud.base import CrudBase
from models import Anime
from schemas import AnimeCreate, AnimeUpdate


class CrudAnime(CrudBase[Anime, AnimeCreate, AnimeUpdate]):
    def __init__(self, Model: type[Anime]):
        super().__init__(Model)

    def is_anime(self, db: Session, anime_id: int) -> bool:
        return self.get(db, anime_id) != None

    def search_by_name(self, db: Session, query: str, limit: int = 10) -> list[Anime]:
        """Search for anime by name with a limit of results."""
        return (
            db.query(Anime)
            .filter(Anime.name.ilike(f"%{query}%"))
            .limit(limit)
            .all()
        )
    
    def get_by_limit(self, db: Session, limit: int = 10) -> list[Anime]:
        """Return 10 random anime."""
        return (
            db.query(Anime).limit(limit).all()
        )