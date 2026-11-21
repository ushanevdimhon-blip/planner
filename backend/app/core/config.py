from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXP_MINUTES: int

    class Config:
        env_file = BASE_DIR / ".env"


settings = Settings()