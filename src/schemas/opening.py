from typing import Optional

from pydantic import BaseModel, HttpUrl, Field


class OpeningPost(BaseModel):
    name: str
    anime_id: int =  Field(alias="animeId")
    artist_ids: list[int] =  Field(alias="artistIds")
    youtube_embed_link: HttpUrl =  Field(alias="youtubeEmbedLink")


class OpeningCreate(BaseModel):
    name: str
    anime_id: int
    youtube_embed_link: str

    @classmethod
    def convert_from_opening_post(cls, opening_post: OpeningPost):
        return cls(
            name=opening_post.name,
            anime_id=opening_post.anime_id,
            youtube_embed_link=str(opening_post.youtube_embed_link)
        )


class OpeningUpdate(BaseModel):
    name: Optional[str] = None
    thumbnail_path: Optional[str] = None


class OpeningPreviewOut(BaseModel):
    id: int
    name: str
    thumbnail_link: HttpUrl = Field(alias="thumbnailLink")

    class Config:
        populate_by_name = True


class OpeningOut(BaseModel):
    id: int
    name: str
    anime_id: int
    artist_ids: list[int]
    youtube_embed_link: HttpUrl
    thumbnail_link: HttpUrl
