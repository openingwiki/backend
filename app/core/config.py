"""
Project settings.
"""
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Models settings.
    model_config = ConfigDict(case_sensitive=True)
    # API settings.
    API_DOMAIN: str = ""

    # Email settings.
    EMAIL_DOMEN_NAME: str = ""
    MAILGUN_API_KEY: str = ""

    # Database settings.
    SQLALCHEMY_DATABASE_URI: str = ""

    # Security settings.
    TOKEN_LENGHT_IN_BYTES: int = 0  # x2 symbols.
    EMAIL_CONFIRM_TOKEN_EXPIRING_SECONDS: int = 0  # 3 hours.

    # Redis settings.
    REDIS_HOST: str = ""
    REDIS_PORT: int = 0

    # Testing settings.
    IS_SETTINGS_FOR_TEST: bool = True


settings = Settings()
