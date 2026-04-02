"""API authentication dependencies."""

import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from fastapi_production_template.core.settings import get_settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(x_api_key: str | None = Security(api_key_header)) -> None:
    """Validate `X-API-Key` header against configured key."""

    expected = get_settings().api_key
    if not x_api_key or not secrets.compare_digest(x_api_key, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
