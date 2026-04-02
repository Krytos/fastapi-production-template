"""Application factory and FastAPI setup."""

from fastapi import FastAPI

from fastapi_production_template.api.v1.router import build_router
from fastapi_production_template.core.settings import get_settings
from fastapi_production_template.services.document_service import create_seeded_service


def create_app() -> FastAPI:
    """Create and configure a FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """

    settings = get_settings()
    document_service = create_seeded_service()
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.include_router(build_router(settings=settings, document_service=document_service), prefix=settings.api_prefix)
    return app


app: FastAPI = create_app()
