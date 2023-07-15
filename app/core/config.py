from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Email settings.
    EMAIL_DOMEN_NAME: str = ""    
    MAILGUN_API_KEY: str = ""

    class Config:
        case_sensitive = True
