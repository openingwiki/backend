from pathlib import Path
from distutils.util import strtobool

from dotenv import dotenv_values

# .env file must be placed in src folder.
config = dotenv_values(".env")

class Settings:
    DATABASE_URL = config["DATABASE_URL"]
    DROP_DATABASE_EVERY_LAUNCH = bool(strtobool(config["IS_SETTINGS_FOR_TESTS"]))
    CORS_ORIGINS = config["CORS_ORIGINS"].split(",")

    API_REQUEST_PREFIX = config["API_REQUEST_PREFIX"]
    TOKEN_LENGHT_IN_BYTES = 256
    PATH_TO_THUMBNAILS = Path(config["PATH_TO_THUMBNAILS"])
    PATH_TO_ANIME_PREVIEWS = Path(config["PATH_TO_ANIME_PREVIEWS"])

    IS_HTTPS = bool(strtobool(config["IS_HTTPS"])) 


settings = Settings()