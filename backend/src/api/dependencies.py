"""Dependency injection providers for FastAPI."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.config.database import AsyncSessionLocal


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


# Repository factory dependencies (to be implemented in Phase 3)
# def get_notebook_repository(db: AsyncSession = Depends(get_db)) -> INotebookRepository:
#     """Get notebook repository instance."""
#     return NotebookRepository(db)

# def get_section_repository(db: AsyncSession = Depends(get_db)) -> ISectionRepository:
#     """Get section repository instance."""
#     return SectionRepository(db)

# def get_page_repository(db: AsyncSession = Depends(get_db)) -> IPageRepository:
#     """Get page repository instance."""
#     return PageRepository(db)

# def get_tag_repository(db: AsyncSession = Depends(get_db)) -> ITagRepository:
#     """Get tag repository instance."""
#     return TagRepository(db)
