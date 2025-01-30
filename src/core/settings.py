from dotenv import dotenv_values

# .env file must be placed in src folder.
config = dotenv_values(".env")

class Settings:
    DATABASE_URL = config["DATABASE_URL"]

    API_REQUEST_PREFIX = "/api"
    TOKEN_LENGHT_IN_BYTES = 256

    DROP_DATABASE_EVERY_LAUNCH = True

settings = Settings()