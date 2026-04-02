"""Pytest shared fixtures."""

import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

SRC_PATH = Path(__file__).resolve().parents[1] / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


@pytest.fixture()
def api_key() -> str:
    """Provide test API key."""

    return "test-api-key"


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, api_key: str) -> Generator[TestClient]:
    """Provide FastAPI test client.

    Returns:
        Generator[TestClient, None, None]: Yielded test client.
    """

    database_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{database_path.as_posix()}")
    monkeypatch.setenv("API_KEY", api_key)
    monkeypatch.setenv("APP_NAME", "FastAPI Production Template (Test)")
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("LOG_LEVEL", "INFO")

    from fastapi_production_template.core.settings import get_settings
    from fastapi_production_template.main import create_app

    get_settings.cache_clear()
    with TestClient(create_app()) as test_client:
        yield test_client
    get_settings.cache_clear()
