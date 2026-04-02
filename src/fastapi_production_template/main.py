"""Application factory and FastAPI setup."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_production_template.api.v1.router import build_router
from fastapi_production_template.core.logging import configure_logging
from fastapi_production_template.core.settings import get_settings
from fastapi_production_template.db.engine import create_async_database_engine, create_postgres_session_factory
from fastapi_production_template.db.models import Base
from fastapi_production_template.middleware.request_id import RequestIdMiddleware
from fastapi_production_template.observability.metrics import MetricsStore
from fastapi_production_template.services.document_service import create_document_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and teardown long-lived resources."""

    settings = get_settings()
    engine = create_async_database_engine(database_url=settings.database_url, echo=False)
    app.state.engine = engine
    app.state.session_factory = create_postgres_session_factory(engine=engine)

    # PoC template mode: create schema at startup from ORM metadata.
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        await app.state.engine.dispose()


def create_app() -> FastAPI:
    """Create and configure a FastAPI application."""

    settings = get_settings()
    configure_logging(level=settings.log_level)

    metrics = MetricsStore()
    document_service = create_document_service()
    app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
    app.add_middleware(RequestIdMiddleware, metrics=metrics)
    app.include_router(
        build_router(settings=settings, document_service=document_service, metrics=metrics),
        prefix=settings.api_prefix,
    )
    return app


app: FastAPI = create_app()
