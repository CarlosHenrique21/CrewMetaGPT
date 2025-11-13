import os

from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    app_name: str = "URL Shortener API"
    database_url: AnyUrl = "sqlite+aiosqlite:///./test.db"  # Placeholder SQLite for MVP
    base_url: str = "http://localhost:8000"  # Base domain for short URLs

    class Config:
        env_file = ".env"


settings = Settings()
