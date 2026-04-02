"""Integration tests for API routes."""

from fastapi.testclient import TestClient


def _auth_headers(api_key: str) -> dict[str, str]:
    return {"X-API-Key": api_key}


def test_health(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    payload = response.json()
    assert response.status_code == 200
    assert payload["status"] == "ok"


def test_metrics_open_and_contains_counters(client: TestClient) -> None:
    health_response = client.get("/api/v1/health")
    assert health_response.status_code == 200
    not_found_response = client.get("/api/v1/not-a-real-route")
    assert not_found_response.status_code == 404
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    assert "# HELP http_requests_total" in response.text
    assert 'http_requests_total{method="GET",path="/api/v1/health",status="200"}' in response.text
    assert 'http_request_duration_seconds_total{method="GET",path="/api/v1/health",status="200"}' in response.text
    assert 'http_requests_total{method="GET",path="/api/v1/not-a-real-route",status="404"}' in response.text
    assert "http_requests_in_flight" in response.text


def test_document_routes_require_api_key(client: TestClient) -> None:
    response = client.get("/api/v1/documents")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


def test_document_crud_and_analyze(client: TestClient, api_key: str) -> None:
    create_response = client.post(
        "/api/v1/documents",
        json={"document_id": "doc-001", "content": "alpha beta gamma"},
        headers=_auth_headers(api_key),
    )
    assert create_response.status_code == 200
    created_payload = create_response.json()
    assert created_payload["document_id"] == "doc-001"
    assert created_payload["content"] == "alpha beta gamma"

    duplicate_response = client.post(
        "/api/v1/documents",
        json={"document_id": "doc-001", "content": "duplicate"},
        headers=_auth_headers(api_key),
    )
    assert duplicate_response.status_code == 409

    list_response = client.get("/api/v1/documents", headers=_auth_headers(api_key))
    assert list_response.status_code == 200
    listed_payload = list_response.json()
    assert len(listed_payload["documents"]) == 1
    assert listed_payload["documents"][0]["document_id"] == "doc-001"

    get_response = client.get("/api/v1/documents/doc-001", headers=_auth_headers(api_key))
    assert get_response.status_code == 200
    get_payload = get_response.json()
    assert get_payload["document_id"] == "doc-001"
    assert get_payload["preview"] == "alpha beta gamma"

    update_response = client.put(
        "/api/v1/documents/doc-001",
        json={"content": "beta gamma delta"},
        headers=_auth_headers(api_key),
    )
    assert update_response.status_code == 200
    assert update_response.json()["content"] == "beta gamma delta"

    analyze_response = client.post(
        "/api/v1/documents/analyze",
        json={"content": "alpha beta gamma", "strategy": "keywords"},
        headers=_auth_headers(api_key),
    )
    assert analyze_response.status_code == 200
    analyzed_payload = analyze_response.json()
    assert analyzed_payload["strategy"] == "keywords"
    assert analyzed_payload["word_count"] == 3

    delete_response = client.delete("/api/v1/documents/doc-001", headers=_auth_headers(api_key))
    assert delete_response.status_code == 204

    missing_response = client.get("/api/v1/documents/doc-001", headers=_auth_headers(api_key))
    assert missing_response.status_code == 404

    missing_update_response = client.put(
        "/api/v1/documents/missing",
        json={"content": "not found"},
        headers=_auth_headers(api_key),
    )
    assert missing_update_response.status_code == 404

    missing_delete_response = client.delete("/api/v1/documents/missing", headers=_auth_headers(api_key))
    assert missing_delete_response.status_code == 404

    metrics_response = client.get("/api/v1/metrics")
    assert metrics_response.status_code == 200
    assert (
        'http_requests_total{method="GET",path="/api/v1/documents/{document_id}",status="200"}' in metrics_response.text
    )


def test_request_id_header_echo(client: TestClient) -> None:
    response = client.get("/api/v1/health", headers={"X-Request-ID": "custom-id-123"})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "custom-id-123"
