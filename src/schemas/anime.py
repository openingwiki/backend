from pydantic import BaseModel

class AnimePost(BaseModel):
    name: str

class AnimeCreate(BaseModel):
    name: str

    @classmethod
    def convert_from_anime_post(cls, anime_post: AnimePost):
        return cls(
            name=anime_post.name,
        )



class AnimeOut(BaseModel):
    id: int
    name: str


class AnimeUpdate(BaseModel):
    pass