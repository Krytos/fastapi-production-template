"""Unit tests for database engine helpers."""

import pytest

from fastapi_production_template.db.engine import (
    create_postgres_async_engine,
    create_postgres_session_factory,
    normalize_postgres_async_url,
)


def test_normalize_postgres_url_sets_asyncpg_driver() -> None:
    """Convert postgres URL to asyncpg URL when no driver is provided."""

    result = normalize_postgres_async_url("postgresql://user:pass@localhost:5432/app")
    assert result == "postgresql+asyncpg://user:pass@localhost:5432/app"


def test_normalize_postgres_url_keeps_asyncpg_driver() -> None:
    """Leave asyncpg URLs unchanged."""

    source = "postgresql+asyncpg://user:pass@localhost:5432/app"
    assert normalize_postgres_async_url(source) == source


def test_normalize_postgres_url_rejects_non_postgres() -> None:
    """Reject non-postgres URL dialects."""

    with pytest.raises(ValueError, match="postgres dialect"):
        normalize_postgres_async_url("sqlite:///tmp.db")


def test_create_postgres_async_engine_uses_asyncpg_url() -> None:
    """Create async engine using normalized asyncpg URL."""

    engine = create_postgres_async_engine(database_url="postgresql://user:pass@localhost:5432/app")
    assert str(engine.url) == "postgresql+asyncpg://user:***@localhost:5432/app"


def test_create_postgres_session_factory_binds_engine() -> None:
    """Bind a session factory to the provided engine."""

    engine = create_postgres_async_engine(database_url="postgresql://user:pass@localhost:5432/app")
    session_factory = create_postgres_session_factory(engine=engine)
    assert session_factory.kw["bind"] is engine
