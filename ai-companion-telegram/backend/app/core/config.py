"""
Core configuration settings for the AI Companion application.
Loads environment variables and provides type-safe access.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    POSTGRES_USER: str = "aiuser"
    POSTGRES_PASSWORD: str = "aipassword"
    POSTGRES_DB: str = "ai_companion"
    DATABASE_URL: Optional[str] = None

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Ollama Configuration (Local or Cloud)
    # For local: http://localhost:11434
    # For cloud: https://api.ollama.cloud
    OLLAMA_HOST: str = "https://api.ollama.cloud"
    OLLAMA_MODEL: str = "qwen2.5:14b"
    OLLAMA_API_KEY: Optional[str] = None  # Required for Ollama Cloud
    USE_OLLAMA_CLOUD: bool = True  # Set to False for local Ollama

    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_WEBHOOK_SECRET: Optional[str] = None

    # External APIs
    TAVILY_API_KEY: Optional[str] = None

    # Application
    APP_ENV: str = "development"
    SECRET_KEY: str = "your-secret-key-change-in-production"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_database_url(self) -> str:
        """Get database URL, constructing from components if not provided directly."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:5432/{self.POSTGRES_DB}"

    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.APP_ENV == "development"


# Global settings instance
settings = Settings()
