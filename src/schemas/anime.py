from pydantic import BaseModel

from models import Anime


class AnimePost(BaseModel):
    name: str

class AnimeCreate(BaseModel):
    name: str

    @classmethod
    def convert_from_anime_post(cls, anime_post: AnimePost) -> "AnimeCreate":
        return cls(
            name=anime_post.name,
        )



class AnimeOut(BaseModel):
    id: int
    name: str


class AnimePreviewOut(BaseModel):
    id: int
    name: str
    
    @classmethod
    def convert_from_anime(cls, anime: Anime) -> "AnimePreviewOut":
        return cls(
            id=anime.id,
            name=anime.name
        )

class AnimeUpdate(BaseModel):
    pass