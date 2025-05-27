from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPEN_METEO_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
