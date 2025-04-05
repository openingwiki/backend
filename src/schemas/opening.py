from typing import Optional

from pydantic import BaseModel, HttpUrl, Field

import utils
from models import Opening


def extract_youtube_id(youtube_embed_link: str) -> str:
    return youtube_embed_link.split("/")[-1]

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
    def convert_from_opening_post(cls, opening_post: OpeningPost) -> "OpeningCreate":
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
    anime_name: str = Field(alias="animeName")
    artist_names: list[str] = Field(alias="artistNames")

    @classmethod
    def convert_from_opening(opening: Opening) -> "OpeningPreviewOut":
        return OpeningPreviewOut(
            id=opening.id,
            name=opening.name,
            anime_name=opening.anime.name,
            artist_names=[artist.name for artist in opening.artists],
            thumbnail_link=HttpUrl(utils.get_youtube_preview_by_embed_link(opening.youtube_embed_link))
        )

    class Config:
        populate_by_name = True


class OpeningOut(BaseModel):
    id: int
    name: str
    anime_id: int
    artist_ids: list[int]
    youtube_embed_link: HttpUrl
    thumbnail_link: HttpUrl

    @classmethod
    def convert_from_opening(opening: Opening) -> "OpeningOut":
        return OpeningOut(
            id=opening.id,
            name=opening.name,
            anime_id=opening.anime_id,
            artist_ids=[artist.id for artist in opening.artists],
            youtube_embed_link=HttpUrl(opening.youtube_embed_link),
            thumbnail_link=HttpUrl(
                utils.get_youtube_preview_by_embed_link(opening.youtube_embed_link)
            )
        )