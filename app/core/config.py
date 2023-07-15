from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Email settings.
    EMAIL_DOMEN_NAME: str = ""    
    MAILGUN_API_KEY: str = ""
    
    # Database settings.
    SQLALCHEMY_DATABASE_URI: str = ""

    # Access token settings.
    ENCRYPTING_ALGORITHM: str = "" 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0
    SECRET_KEY: str = ""
    PASSWORD_SALT: str = "" 

    class Config:
        case_sensitive = True
    

settings = Settings()