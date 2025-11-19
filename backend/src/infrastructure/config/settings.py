"""Application settings using Pydantic."""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "Notebook Management"
    debug: bool = True
    environment: str = "development"

    # Database
    database_url: str = "sqlite+aiosqlite:///./notebooks.db"

    # File Storage
    upload_dir: str = "./static/uploads"
    max_upload_size_mb: int = 5

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    cors_origins: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]

    # Auto-save
    auto_save_interval_ms: int = 3000

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
