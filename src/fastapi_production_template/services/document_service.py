"""Document analysis business logic."""

from dataclasses import dataclass

from fastapi_production_template.domain.models import AnalyzeResponse, Document, DocumentResponse


@dataclass(kw_only=True)
class DocumentService:
    """Service that analyzes and retrieves documents.

    Args:
        documents (dict[str, Document]): In-memory document store.
    """

    documents: dict[str, Document]

    def analyze_document(self, *, content: str, strategy: str) -> AnalyzeResponse:
        """Analyze text using a selected strategy.

        Args:
            content (str): Text input for analysis.
            strategy (str): Strategy selector.

        Returns:
            AnalyzeResponse: Analysis result.
        """

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

    def get_document(self, *, document_id: str) -> DocumentResponse | None:
        """Fetch a document and create a response projection.

        Args:
            document_id (str): Identifier of the document.

        Returns:
            DocumentResponse | None: Response model if found, otherwise None.
        """

        if not (document := self.documents.get(document_id)):
            return None
        preview: str = document.content[:80]
        return DocumentResponse(document_id=document.document_id, preview=preview, characters=len(document.content))


def create_seeded_service() -> DocumentService:
    """Create a service instance with seeded documents.

    Returns:
        DocumentService: Service with default in-memory data.
    """

    documents: dict[str, Document] = {
            "doc-001": Document(
                    document_id="doc-001",
                    content="FastAPI with CI and Terraform is a strong production baseline for modern backend teams.",
            ),
            "doc-002": Document(
                    document_id="doc-002",
                    content="Typed Python services are easier to maintain, test, and evolve in active repositories.",
            ),
    }
    return DocumentService(documents=documents)
