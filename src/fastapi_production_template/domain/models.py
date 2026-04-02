"""Domain request/response models."""

from datetime import datetime

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Input payload for document analysis.

    Args:
        content (str): Raw text to analyze.
        strategy (str): Analysis strategy selector.
    """

    content: str = Field(min_length=1, max_length=5000)
    strategy: str = Field(default="summary")


class AnalyzeResponse(BaseModel):
    """Result payload for document analysis.

    Args:
        strategy (str): Strategy that produced the result.
        result (str): Human-readable analysis output.
        word_count (int): Number of words in input.
    """

    strategy: str
    result: str
    word_count: int


class DocumentResponse(BaseModel):
    """Response payload for document retrieval.

    Args:
        document_id (str): Stable document identifier.
        preview (str): Content preview.
        characters (int): Character count.
    """

    document_id: str
    preview: str
    characters: int


class DocumentCreateRequest(BaseModel):
    """Input payload for document creation."""

    document_id: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1, max_length=5000)


class DocumentUpdateRequest(BaseModel):
    """Input payload for document updates."""

    content: str = Field(min_length=1, max_length=5000)


class DocumentRecordResponse(BaseModel):
    """Document payload backed by database persistence."""

    document_id: str
    content: str
    created_at: datetime
    updated_at: datetime


class DocumentListResponse(BaseModel):
    """Response payload for list endpoint."""

    documents: list[DocumentRecordResponse]


class HealthResponse(BaseModel):
    """Health endpoint response model.

    Args:
        name (str): Application name.
        environment (str): Deployment environment.
        status (str): Health status string.
    """

    name: str
    environment: str
    status: str
