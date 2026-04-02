"""Application settings management."""

from dataclasses import dataclass
from os import getenv


@dataclass(kw_only=True)
class Settings:
    """Runtime settings loaded from environment variables.

    Args:
        app_name (str): Public application name.
        environment (str): Deployment environment identifier.
        database_url (str): SQLAlchemy-compatible database URL.
        api_prefix (str): API route prefix.

    Side Effects:
        Reads process environment variables.
    """

    app_name: str
    environment: str
    database_url: str
    api_prefix: str


def get_settings() -> Settings:
    """Create settings from environment variables.

    Returns:
        Settings: Loaded and normalized settings object.

    Side Effects:
        Reads process environment variables.
    """

    environment: str = getenv("ENVIRONMENT", "development")
    database_url: str = getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://fastapi:fastapi@localhost:5432/fastapi_template",
    )
    return Settings(
        app_name=getenv("APP_NAME", "FastAPI Production Template"),
        environment=environment,
        database_url=database_url,
        api_prefix=getenv("API_PREFIX", "/api/v1"),
    )
