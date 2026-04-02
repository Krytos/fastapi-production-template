"""Application settings management."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = Field(default="FastAPI Production Template", alias="APP_NAME")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    database_url: str = Field(
        default="postgresql+asyncpg://fastapi:fastapi@localhost:5432/fastapi_template",
        alias="DATABASE_URL",
    )
    api_prefix: str = Field(default="/api/v1", alias="API_PREFIX")
    api_key: str = Field(default="dev-api-key", alias="API_KEY")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load and cache application settings."""

    return Settings()
