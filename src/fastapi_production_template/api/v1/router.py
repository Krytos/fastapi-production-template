"""Versioned API routes."""


from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import PlainTextResponse

from fastapi_production_template.api.auth import require_api_key
from fastapi_production_template.core.settings import Settings
from fastapi_production_template.db.repository import DocumentRepository
from fastapi_production_template.db.session import get_document_repository
from fastapi_production_template.domain.models import (
    AnalyzeRequest,
    AnalyzeResponse,
    DocumentCreateRequest,
    DocumentListResponse,
    DocumentRecordResponse,
    DocumentResponse,
    DocumentUpdateRequest,
    HealthResponse,
)
from fastapi_production_template.observability.metrics import MetricsStore
from fastapi_production_template.services.document_service import DocumentService


def _to_record_response(record) -> DocumentRecordResponse:
    return DocumentRecordResponse(
        document_id=record.document_id,
        content=record.content,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


def build_router(*, settings: Settings, document_service: DocumentService, metrics: MetricsStore) -> APIRouter:
    """Create API router with all endpoints."""

    router: APIRouter = APIRouter()
    protected = [Depends(require_api_key)]

    @router.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(name=settings.app_name, environment=settings.environment, status="ok")

    @router.get("/metrics", response_class=PlainTextResponse)
    async def metrics_endpoint() -> str:
        return metrics.render()

    @router.post("/documents/analyze", response_model=AnalyzeResponse, dependencies=protected)
    async def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
        return document_service.analyze_document(content=payload.content, strategy=payload.strategy)

    @router.post("/documents", response_model=DocumentRecordResponse, dependencies=protected)
    async def create_document(
        payload: DocumentCreateRequest,
        repository: Annotated[DocumentRepository, Depends(get_document_repository)],
    ) -> DocumentRecordResponse:
        existing = await repository.get(document_id=payload.document_id)
        if existing is not None:
            raise HTTPException(status_code=409, detail=f"Document '{payload.document_id}' already exists")
        record = await repository.create(document_id=payload.document_id, content=payload.content)
        return _to_record_response(record)

    @router.get("/documents", response_model=DocumentListResponse, dependencies=protected)
    async def list_documents(
        repository: Annotated[DocumentRepository, Depends(get_document_repository)],
    ) -> DocumentListResponse:
        records = await repository.list()
        return DocumentListResponse(documents=[_to_record_response(record) for record in records])

    @router.get("/documents/{document_id}", response_model=DocumentResponse, dependencies=protected)
    async def get_document(
        document_id: str,
        repository: Annotated[DocumentRepository, Depends(get_document_repository)],
    ) -> DocumentResponse:
        record = await repository.get(document_id=document_id)
        if record is None:
            raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found")
        preview: str = record.content[:80]
        return DocumentResponse(document_id=record.document_id, preview=preview, characters=len(record.content))

    @router.put("/documents/{document_id}", response_model=DocumentRecordResponse, dependencies=protected)
    async def update_document(
        document_id: str,
        payload: DocumentUpdateRequest,
        repository: Annotated[DocumentRepository, Depends(get_document_repository)],
    ) -> DocumentRecordResponse:
        record = await repository.update(document_id=document_id, content=payload.content)
        if record is None:
            raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found")
        return _to_record_response(record)

    @router.delete("/documents/{document_id}", status_code=204, dependencies=protected)
    async def delete_document(
        document_id: str,
        repository: Annotated[DocumentRepository, Depends(get_document_repository)],
    ) -> Response:
        deleted = await repository.delete(document_id=document_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found")
        return Response(status_code=204)

    return router
