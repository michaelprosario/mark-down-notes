"""Application settings using Pydantic."""

from functools import lru_cache
from typing import List
from pydantic import field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation."""

    # Application
    app_name: str = "Notebook Management"
    debug: bool = True
    environment: str = Field(default="development", pattern="^(development|staging|production)$")

    # Database
    database_url: str = "sqlite+aiosqlite:///./notebooks.db"

    # File Storage
    upload_dir: str = "./static/uploads"
    max_upload_size_mb: int = Field(default=5, ge=1, le=100)

    # Security
    secret_key: str = Field(default="your-secret-key-change-in-production", min_length=32)
    cors_origins: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]

    # Auto-save
    auto_save_interval_ms: int = Field(default=3000, ge=1000, le=60000)

    # Server
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)
    reload: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v or not v.strip():
            raise ValueError("Database URL cannot be empty")
        
        # Check for supported databases
        supported_prefixes = ["sqlite+aiosqlite://", "postgresql+asyncpg://", "postgresql://"]
        if not any(v.startswith(prefix) for prefix in supported_prefixes):
            raise ValueError(
                f"Database URL must start with one of: {', '.join(supported_prefixes)}"
            )
        
        return v

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str, info) -> str:
        """Validate secret key in production."""
        if info.data.get("environment") == "production":
            if v == "your-secret-key-change-in-production":
                raise ValueError("Must set a secure secret key in production")
        return v


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
