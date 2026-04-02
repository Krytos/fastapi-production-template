"""Versioned API routes."""

from fastapi import APIRouter, HTTPException

from fastapi_production_template.core.settings import Settings
from fastapi_production_template.domain.models import AnalyzeRequest, AnalyzeResponse, DocumentResponse, HealthResponse
from fastapi_production_template.services.document_service import DocumentService


def build_router(*, settings: Settings, document_service: DocumentService) -> APIRouter:
    """Create API router with all endpoints.

    Args:
        settings (Settings): Runtime configuration.
        document_service (DocumentService): Service dependency.

    Returns:
        APIRouter: Configured API router.
    """

    router: APIRouter = APIRouter()

    @router.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        """Return service health state.

        Returns:
            HealthResponse: Current health payload.
        """

        return HealthResponse(name=settings.app_name, environment=settings.environment, status="ok")

    @router.post("/documents/analyze", response_model=AnalyzeResponse)
    def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
        """Analyze document content.

        Args:
            payload (AnalyzeRequest): Request payload.

        Returns:
            AnalyzeResponse: Analysis response payload.
        """

        return document_service.analyze_document(content=payload.content, strategy=payload.strategy)

    @router.get("/documents/{document_id}", response_model=DocumentResponse)
    def get_document(document_id: str) -> DocumentResponse:
        """Fetch a document by identifier.

        Args:
            document_id (str): Document identifier.

        Returns:
            DocumentResponse: Retrieved document view.

        Raises:
            HTTPException: If the document does not exist.
        """

        if not (document := document_service.get_document(document_id=document_id)):
            raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found")
        return document

    return router
