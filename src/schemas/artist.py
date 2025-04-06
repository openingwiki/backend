from pydantic import BaseModel

from models import Artist


class ArtistPost(BaseModel):
    name: str


class ArtistCreate(BaseModel):
    name: str

    @classmethod
    def convert_from_artist_post(cls, artist_post: ArtistPost):
        return cls(
            name=artist_post.name,
        )


class ArtistOut(BaseModel):
    id: int
    name: str


class ArtistPreviewOut(BaseModel):
    id: int
    name: str

    @classmethod
    def convert_from_artist(cls, artist: Artist):
        return cls(
            id=artist.id,
            name=artist.name
        )


class ArtistUpdate(BaseModel):
    pass