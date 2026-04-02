"""Document analysis business logic."""

from dataclasses import dataclass

from fastapi_production_template.domain.models import AnalyzeResponse


@dataclass(kw_only=True)
class DocumentService:
    """Service that performs document analysis."""

    def analyze_document(self, *, content: str, strategy: str) -> AnalyzeResponse:
        """Analyze text using a selected strategy."""

        words: list[str] = content.split()
        word_count: int = len(words)
        match strategy:
            case "summary":
                first_words: str = " ".join(words[:12])
                result: str = f"Summary: {first_words}" if first_words else "Summary:"
            case "keywords":
                unique: list[str] = sorted(set(word.lower().strip(".,!?") for word in words if word))
                result = f"Keywords: {', '.join(unique[:6])}"
            case _:
                result = f"Fallback strategy '{strategy}' used"
        return AnalyzeResponse(strategy=strategy, result=result, word_count=word_count)


def create_document_service() -> DocumentService:
    """Create a stateless document service."""

    return DocumentService()
