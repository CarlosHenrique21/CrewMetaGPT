import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "API REST para Gerenciar Tarefas"
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'

    # Database
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', 5432))
    DB_USER: str = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'password')
    DB_NAME: str = os.getenv('DB_NAME', 'task_manager')

    # JWT
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'supersecretjwtkey')
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Pagination
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

settings = Settings()
