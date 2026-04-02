"""Async repository for document persistence."""


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_production_template.db.models import DocumentRecord


class DocumentRepository:
    """CRUD access for documents table."""

    def __init__(self, *, session: AsyncSession) -> None:
        self._session = session

    async def create(self, *, document_id: str, content: str) -> DocumentRecord:
        record = DocumentRecord(document_id=document_id, content=content)
        self._session.add(record)
        await self._session.commit()
        await self._session.refresh(record)
        return record

    async def get(self, *, document_id: str) -> DocumentRecord | None:
        return await self._session.get(DocumentRecord, document_id)

    async def update(self, *, document_id: str, content: str) -> DocumentRecord | None:
        record = await self.get(document_id=document_id)
        if record is None:
            return None
        record.content = content
        await self._session.commit()
        await self._session.refresh(record)
        return record

    async def delete(self, *, document_id: str) -> bool:
        record = await self.get(document_id=document_id)
        if record is None:
            return False
        await self._session.delete(record)
        await self._session.commit()
        return True

    async def list(self, *, limit: int = 100, offset: int = 0) -> list[DocumentRecord]:
        stmt = (
            select(DocumentRecord)
            .order_by(DocumentRecord.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
