from typing import Optional

from pydantic import BaseModel, HttpUrl


class OpeningPost(BaseModel):
    name: str
    anime_id: int
    youtube_embed_link: HttpUrl


class OpeningCreate(BaseModel):
    name: str
    anime_id: int
    youtube_embed_link: str
    thumbnail_path: Optional[str] = None

    @classmethod
    def convert_from_opening_post(cls, opening_post: OpeningPost):
        return cls(
            name=opening_post.name,
            anime_id=opening_post.anime_id,
            youtube_embed_link=opening_post.youtube_embed_link
        )


class OpeningUpdate(BaseModel):
    name: Optional[str] = None
    thumbnail_path: Optional[str] = None


class OpeningOut(BaseModel):
    name: str
    anime_id: int
    youtube_embed_link: str
    thumbnail_path: str
