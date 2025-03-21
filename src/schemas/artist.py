from pydantic import BaseModel


class ArtistPost(BaseModel):
    name: str

class ArtistCreate(BaseModel):
    name: str

    @classmethod
    def convert_from_artist_post(cls, artist_post):
        return cls(
            name=artist_post.name,
        )

class ArtistOut(BaseModel):
    id: int
    name: str


class ArtistUpdate(BaseModel):
    pass