"""Dependency utilities for db sessions and repositories."""


from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from fastapi_production_template.db.repository import DocumentRepository


def get_session_factory(request: Request) -> async_sessionmaker[AsyncSession]:
    """Return configured session factory from app state."""

    return request.app.state.session_factory


async def get_session(
    session_factory: Annotated[async_sessionmaker[AsyncSession], Depends(get_session_factory)],
) -> AsyncGenerator[AsyncSession]:
    """Yield a db session for request scope."""

    async with session_factory() as session:
        yield session


async def get_document_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DocumentRepository:
    """Build repository instance from active session."""

    return DocumentRepository(session=session)
