from dotenv import dotenv_values

# .env file must be placed in src folder.
config = dotenv_values(".env")

class Settings:
    DATABASE_URL = config["DATABASE_URL"]

    API_REQUEST_PREFIX = "/api"
    