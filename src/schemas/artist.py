from pydantic import BaseModel


class ArtistCreate(BaseModel):
    name: str


class ArtistOut(BaseModel):
    id: int
    name: str


class ArtistUpdate(BaseModel):
    pass