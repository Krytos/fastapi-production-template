"""SQLAlchemy async engine and session factory helpers."""

from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


def normalize_postgres_async_url(database_url: str) -> str:
    """Normalize postgres URLs so SQLAlchemy async engine uses asyncpg.

    Args:
        database_url (str): Input database URL.

    Returns:
        str: URL guaranteed to use the ``postgresql+asyncpg`` driver.

    Raises:
        ValueError: If URL dialect is not postgres.
    """

    parsed = make_url(database_url)
    backend = parsed.get_backend_name()
    if backend not in {"postgresql", "postgres"}:
        raise ValueError("Database URL must use a postgres dialect")

    if parsed.get_driver_name() != "asyncpg":
        parsed = parsed.set(drivername="postgresql+asyncpg")
    return parsed.render_as_string(hide_password=False)


def create_postgres_async_engine(*, database_url: str, echo: bool = False) -> AsyncEngine:
    """Create a SQLAlchemy async engine for postgres.

    Args:
        database_url (str): SQLAlchemy-compatible postgres URL.
        echo (bool): Whether to log SQL statements.

    Returns:
        AsyncEngine: Configured async engine instance.
    """

    normalized_url = normalize_postgres_async_url(database_url)
    return create_async_engine(normalized_url, echo=echo, pool_pre_ping=True)


def create_postgres_session_factory(*, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create session factory bound to a postgres async engine.

    Args:
        engine (AsyncEngine): SQLAlchemy async engine.

    Returns:
        async_sessionmaker[AsyncSession]: Session maker with safe defaults.
    """

    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
