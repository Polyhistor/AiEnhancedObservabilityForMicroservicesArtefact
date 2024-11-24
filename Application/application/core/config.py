from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Your API Name"
    VERSION: str = "1.0.0"
    
    class Config:
        case_sensitive = True

settings = Settings()