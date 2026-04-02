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
def client() -> Generator[TestClient]:
    """Provide FastAPI test client.

    Returns:
        Generator[TestClient, None, None]: Yielded test client.
    """

    from fastapi_production_template.main import create_app

    with TestClient(create_app()) as test_client:
        yield test_client
