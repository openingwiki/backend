from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API settings.
    API_DOMAIN: str = ""

    # Email settings.
    EMAIL_DOMEN_NAME: str = ""    
    MAILGUN_API_KEY: str = ""
    
    # Database settings.
    SQLALCHEMY_DATABASE_URI: str = ""

    # Security settings.
    PASSWORD_SALT: str = "" 

    # Redis settings.
    REDIS_HOST: str = ""
    REDIS_PORT: int = 0

    class Config:
        case_sensitive = True
    

settings = Settings()