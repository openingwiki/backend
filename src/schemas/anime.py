from pydantic import BaseModel


class AnimeCreate(BaseModel):
    name: str


class AnimeOut(BaseModel):
    id: int
    name: str


class AnimeUpdate(BaseModel):
    pass