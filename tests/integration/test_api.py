"""Integration tests for API routes."""

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    """Validate health endpoint.

    Args:
        client (TestClient): Application test client.

    Returns:
        None: No return value.
    """

    response = client.get("/api/v1/health")
    payload = response.json()
    assert response.status_code == 200
    assert payload["status"] == "ok"


def test_analyze(client: TestClient) -> None:
    """Validate analyze endpoint.

    Args:
        client (TestClient): Application test client.

    Returns:
        None: No return value.
    """

    response = client.post(
        "/api/v1/documents/analyze",
        json={"content": "alpha beta gamma", "strategy": "keywords"},
    )
    payload = response.json()
    assert response.status_code == 200
    assert payload["strategy"] == "keywords"
    assert payload["word_count"] == 3


def test_get_document_success(client: TestClient) -> None:
    """Validate get-document success path.

    Args:
        client (TestClient): Application test client.

    Returns:
        None: No return value.
    """

    response = client.get("/api/v1/documents/doc-001")
    payload = response.json()
    assert response.status_code == 200
    assert payload["document_id"] == "doc-001"


def test_get_document_not_found(client: TestClient) -> None:
    """Validate get-document not-found path.

    Args:
        client (TestClient): Application test client.

    Returns:
        None: No return value.
    """

    response = client.get("/api/v1/documents/missing")
    payload = response.json()
    assert response.status_code == 404
    assert payload["detail"] == "Document 'missing' not found"
