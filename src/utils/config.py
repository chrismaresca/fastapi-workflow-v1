from functools import lru_cache
from typing import Optional, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # OpenAI Settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o"

    # API Settings 
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Chat API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "FastAPI application for AI chat"

    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Environment
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True if ENVIRONMENT == "development" else False

    # AWS Settings
    AWS_REGION: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Creates a cached instance of settings.
    Use this function to get settings throughout the app.
    """
    return Settings()


# Create a settings instance
settings = get_settings()
