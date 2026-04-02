"""Unit tests for logging configuration and app lifespan branches."""

import json
from pathlib import Path

from fastapi.testclient import TestClient
from loguru import logger

from fastapi_production_template.core.logging import configure_logging
from fastapi_production_template.core.settings import get_settings
from fastapi_production_template.main import create_app


def test_configure_logging_emits_json(capsys) -> None:
    configure_logging(level="INFO")
    logger.info("failure")
    captured = capsys.readouterr().out.strip()
    payload = json.loads(captured)
    assert payload["record"]["message"] == "failure"
    assert payload["record"]["extra"]["request_id"] is None


def test_app_lifespan_non_sqlite_database_url(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://fastapi:fastapi@localhost:5432/fastapi_template")
    monkeypatch.setenv("API_KEY", "test-api-key")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    monkeypatch.setenv("APP_NAME", "FastAPI Production Template (Lifespan)")
    monkeypatch.setenv("ENVIRONMENT", "test")
    get_settings.cache_clear()

    with TestClient(create_app()) as client:
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    get_settings.cache_clear()
