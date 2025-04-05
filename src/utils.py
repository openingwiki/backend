from enum import Enum

from sqlalchemy.orm import Session

from schemas import UserCreate, AccessTokenCreate, AnimeCreate, ArtistCreate, OpeningCreate
from core import security, settings
from database import Base, engine
from models import User, AccessToken
from crud import crud_user, crud_access_token, crud_anime, crud_opening, crud_openings_artists, crud_artist


class Role(Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class OpeningStatus(Enum):
    ON_MODERATION = "moderation"
    ACCEPTED = "accepted"


MOCK_USERS = [
    UserCreate(username="admin", hashed_password=security.get_password_hash("admin"), role=Role.ADMIN),
    UserCreate(username="user", hashed_password=security.get_password_hash("user"), role=Role.USER),
    UserCreate(username="moderator", hashed_password=security.get_password_hash("moderator"), role=Role.MODERATOR)
]
MOCK_ACCESS_TOKENS = [
    AccessTokenCreate(user_id=1, token="1")
]
MOCK_ANIME = [
    AnimeCreate(name="Attack on Titan"),
    AnimeCreate(name="Cowboy Bebop"),
    AnimeCreate(name="Vinland Saga"),
]
MOCK_ARTISTS = [
    ArtistCreate(name="Survive Said the Prophet"),
    ArtistCreate(name="Man with a Mission"),
    ArtistCreate(name="Anonymouz"),
    ArtistCreate(name="Linked Horizon"),
    ArtistCreate(name="YOSHIKI"),
    ArtistCreate(name="HYDE"),
    ArtistCreate(name="Shinsei Kamattechan"),
    ArtistCreate(name="SiM"),
    ArtistCreate(name="Seatbelts")
]
MOCK_OPENINGS = [
    OpeningCreate(name="Tank!", anime_id=2, youtube_embed_link="https://www.youtube.com/embed/0hfOyOBHIq4"),
    OpeningCreate(name="Mukanjyo", anime_id=3, youtube_embed_link="https://www.youtube.com/embed/l5wAdQ-UkWY"),
    OpeningCreate(name="Feuerroter Pfeil und Bogen", anime_id=1, youtube_embed_link="https://www.youtube.com/embed/8OkpRK2_gVs")
]
MOCK_OPENINGS_ARTISTS = [
    [1, [9]],
    [2, [1]],
    [3, [4]],
]


def init_db(db: Session):
    # Creating database with mock users in test environment.
    if settings.DROP_DATABASE_EVERY_LAUNCH:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        for mock_user in MOCK_USERS:
            crud_user.create(db, mock_user)
        
        for mock_access_token in MOCK_ACCESS_TOKENS:
            crud_access_token.create(db, mock_access_token)

        for mock_anime in MOCK_ANIME:
            crud_anime.create(db, mock_anime)

        for mock_artist in MOCK_ARTISTS:
            crud_artist.create(db, mock_artist)

        for mock_opening in MOCK_OPENINGS:
            crud_opening.create(db, mock_opening)

        for mock_openings_artists in MOCK_OPENINGS_ARTISTS:
            crud_openings_artists.add_openings_artists(db, *mock_openings_artists)

    else:
        Base.metadata.create_all(bind=engine)


def create_token(db: Session, user: User) -> AccessToken:
    """Utility function to create token"""
    access_token_create = AccessTokenCreate(
        user_id=user.id,
        token=security.create_token(),
    )
    access_token = crud_access_token.create(db, access_token_create)

    return access_token

def extract_youtube_id(youtube_embed_link: str) -> str:
    """Extracting youtube id from youtube embed link"""
    return youtube_embed_link.split("/")[-1]

def get_youtube_preview_by_embed_link(youtube_embed_link: str) -> str:
    """Converting youtube link to it's preview link."""
    return f"https://img.youtube.com/vi/{extract_youtube_id(youtube_embed_link)}/hqdefault.jpg"