"""Unit tests for document service."""

from fastapi_production_template.services.document_service import create_document_service


def test_analyze_summary_strategy() -> None:
    """Validate summary analysis behavior.

    Returns:
        None: No return value.
    """

    service = create_document_service()
    result = service.analyze_document(content="one two three", strategy="summary")
    assert result.strategy == "summary"
    assert result.word_count == 3
    assert result.result == "Summary: one two three"


def test_analyze_keywords_strategy() -> None:
    """Validate keyword strategy behavior.

    Returns:
        None: No return value.
    """

    service = create_document_service()
    result = service.analyze_document(content="Beta alpha beta", strategy="keywords")
    assert result.result == "Keywords: alpha, beta"


def test_analyze_fallback_strategy() -> None:
    """Validate fallback strategy behavior.

    Returns:
        None: No return value.
    """

    service = create_document_service()
    result = service.analyze_document(content="content", strategy="custom")
    assert result.result == "Fallback strategy 'custom' used"
