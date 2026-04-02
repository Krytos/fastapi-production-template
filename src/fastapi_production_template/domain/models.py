"""Domain entities and request/response models."""

from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass(kw_only=True)
class Document:
    """Internal domain model for a document.

    Args:
        document_id (str): Stable document identifier.
        content (str): Raw document content.
    """

    document_id: str
    content: str


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
