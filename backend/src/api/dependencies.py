"""Dependency injection providers for FastAPI."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.config.database import AsyncSessionLocal
from src.infrastructure.data.repositories.notebook_repository import NotebookRepository
from src.infrastructure.data.repositories.section_repository import SectionRepository
from src.infrastructure.data.repositories.page_repository import PageRepository


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency.
    
    Yields:
        AsyncSession: Database session for the request.
    
    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_notebook_repository(db: AsyncSession) -> NotebookRepository:
    """Get notebook repository instance."""
    return NotebookRepository(db)


def get_section_repository(db: AsyncSession) -> SectionRepository:
    """Get section repository instance."""
    return SectionRepository(db)


def get_page_repository(db: AsyncSession) -> PageRepository:
    """Get page repository instance."""
    return PageRepository(db)

