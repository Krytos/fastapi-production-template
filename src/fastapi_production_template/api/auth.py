"""API authentication dependencies."""


import secrets

from fastapi import Header, HTTPException, status

from fastapi_production_template.core.settings import get_settings


async def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Validate `X-API-Key` header against configured key."""

    expected = get_settings().api_key
    if not x_api_key or not secrets.compare_digest(x_api_key, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
