from pathlib import Path

from dotenv import dotenv_values

# .env file must be placed in src folder.
config = dotenv_values(".env")

class Settings:
    DATABASE_URL = config["DATABASE_URL"]

    API_REQUEST_PREFIX = "/api"
    TOKEN_LENGHT_IN_BYTES = 256
    PATH_TO_THUMBNAILS = Path(config["PATH_TO_THUMBNAILS"])
    PATH_TO_ANIME_PREVIEWS = Path(config["PATH_TO_ANIME_PREVIEWS"])

    DROP_DATABASE_EVERY_LAUNCH = True

settings = Settings()