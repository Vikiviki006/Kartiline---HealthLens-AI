"""
Application configuration management using Pydantic Settings.
All configuration is loaded from environment variables / .env file.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────────────────────────
    APP_NAME: str = Field(default="HealthLens AI", description="Application name")
    APP_ENV: Literal["development", "staging", "production"] = Field(
        default="development"
    )
    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: int = Field(default=8000)
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=False)

    # ── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = Field(
        default="postgresql://postgres:password@localhost:5432/healthlens"
    )
    DB_POOL_SIZE: int = Field(default=10)
    DB_MAX_OVERFLOW: int = Field(default=20)
    DB_POOL_TIMEOUT: int = Field(default=30)
    DB_POOL_RECYCLE: int = Field(default=1800)

    # ── Security ─────────────────────────────────────────────────────────
    SECRET_KEY: str = Field(default="change-me-in-production-super-secret-key-32chars")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    # ── CORS ─────────────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"]
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)

    # ── AI Providers ─────────────────────────────────────────────────────
    AI_PROVIDER: Literal["gemini", "openai"] = Field(default="gemini")
    GEMINI_API_KEY: str = Field(default="")
    OPENAI_API_KEY: str = Field(default="")
    OPENAI_MODEL: str = Field(default="gpt-4o-mini")
    GEMINI_MODEL: str = Field(default="gemini-1.5-flash")
    AI_REQUEST_TIMEOUT: int = Field(default=60)
    AI_MAX_RETRIES: int = Field(default=3)

    # ── OCR ──────────────────────────────────────────────────────────────
    OCR_ENGINE: Literal["pdfplumber", "pymupdf", "tesseract"] = Field(
        default="pdfplumber"
    )
    OCR_FALLBACK_ENABLED: bool = Field(default=True)
    TESSERACT_CMD: str = Field(default="tesseract")

    # ── File Storage ─────────────────────────────────────────────────────
    STORAGE_BACKEND: Literal["local", "s3"] = Field(default="local")
    UPLOAD_DIR: str = Field(default="uploads")
    MAX_UPLOAD_SIZE_MB: int = Field(default=20)
    ALLOWED_EXTENSIONS: list[str] = Field(default=[".pdf", ".png", ".jpg", ".jpeg"])

    # ── AWS / S3 ─────────────────────────────────────────────────────────
    S3_BUCKET: str = Field(default="")
    AWS_ACCESS_KEY_ID: str = Field(default="")
    AWS_SECRET_ACCESS_KEY: str = Field(default="")
    AWS_REGION: str = Field(default="us-east-1")

    # ── Logging ──────────────────────────────────────────────────────────
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(default="json")

    # ── Rate Limiting ────────────────────────────────────────────────────
    RATE_LIMIT_ENABLED: bool = Field(default=True)
    RATE_LIMIT_REQUESTS: int = Field(default=100)
    RATE_LIMIT_WINDOW_SECONDS: int = Field(default=60)

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith(("postgresql://", "postgresql+asyncpg://", "sqlite://")):
            raise ValueError("DATABASE_URL must be a PostgreSQL or SQLite connection string")
        return v

    @property
    def max_upload_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()


settings: Settings = get_settings()
