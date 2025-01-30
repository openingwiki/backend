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
