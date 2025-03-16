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
