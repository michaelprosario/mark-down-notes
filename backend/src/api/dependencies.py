"""Dependency injection providers for FastAPI."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.infrastructure.config.database import AsyncSessionLocal
from src.infrastructure.data.repositories.notebook_repository import NotebookRepository
from src.infrastructure.data.repositories.section_repository import SectionRepository
from src.infrastructure.data.repositories.page_repository import PageRepository

# Import services
from src.core.services.create_notebook_service import CreateNotebookService
from src.core.services.update_notebook_service import UpdateNotebookService
from src.core.services.delete_notebook_service import DeleteNotebookService
from src.core.services.get_notebooks_service import GetNotebooksService
from src.core.services.create_section_service import CreateSectionService
from src.core.services.update_section_service import UpdateSectionService
from src.core.services.delete_section_service import DeleteSectionService
from src.core.services.get_sections_service import GetSectionsService
from src.core.services.reorder_sections_service import ReorderSectionsService
from src.core.services.create_page_service import CreatePageService
from src.core.services.update_page_service import UpdatePageService
from src.core.services.delete_page_service import DeletePageService
from src.core.services.get_pages_service import GetPagesService


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


# Repository factories
def get_notebook_repository(db: AsyncSession) -> NotebookRepository:
    """Get notebook repository instance."""
    return NotebookRepository(db)


def get_section_repository(db: AsyncSession) -> SectionRepository:
    """Get section repository instance."""
    return SectionRepository(db)


def get_page_repository(db: AsyncSession) -> PageRepository:
    """Get page repository instance."""
    return PageRepository(db)


# Notebook service factories
def get_create_notebook_service(db: AsyncSession = Depends(get_db)) -> CreateNotebookService:
    """Get create notebook service instance."""
    return CreateNotebookService(get_notebook_repository(db))


def get_update_notebook_service(db: AsyncSession = Depends(get_db)) -> UpdateNotebookService:
    """Get update notebook service instance."""
    return UpdateNotebookService(get_notebook_repository(db))


def get_delete_notebook_service(db: AsyncSession = Depends(get_db)) -> DeleteNotebookService:
    """Get delete notebook service instance."""
    return DeleteNotebookService(get_notebook_repository(db))


def get_get_notebooks_service(db: AsyncSession = Depends(get_db)) -> GetNotebooksService:
    """Get notebooks query service instance."""
    return GetNotebooksService(get_notebook_repository(db))


# Section service factories
def get_create_section_service(db: AsyncSession = Depends(get_db)) -> CreateSectionService:
    """Get create section service instance."""
    return CreateSectionService(get_section_repository(db))


def get_update_section_service(db: AsyncSession = Depends(get_db)) -> UpdateSectionService:
    """Get update section service instance."""
    return UpdateSectionService(get_section_repository(db))


def get_delete_section_service(db: AsyncSession = Depends(get_db)) -> DeleteSectionService:
    """Get delete section service instance."""
    return DeleteSectionService(
        get_section_repository(db),
        get_page_repository(db)
    )


def get_get_sections_service(db: AsyncSession = Depends(get_db)) -> GetSectionsService:
    """Get sections query service instance."""
    return GetSectionsService(get_section_repository(db))


def get_reorder_sections_service(db: AsyncSession = Depends(get_db)) -> ReorderSectionsService:
    """Get reorder sections service instance."""
    return ReorderSectionsService(get_section_repository(db))


# Page service factories
def get_create_page_service(db: AsyncSession = Depends(get_db)) -> CreatePageService:
    """Get create page service instance."""
    return CreatePageService(get_page_repository(db))


def get_update_page_service(db: AsyncSession = Depends(get_db)) -> UpdatePageService:
    """Get update page service instance."""
    return UpdatePageService(get_page_repository(db))


def get_delete_page_service(db: AsyncSession = Depends(get_db)) -> DeletePageService:
    """Get delete page service instance."""
    return DeletePageService(get_page_repository(db))


def get_get_pages_service(db: AsyncSession = Depends(get_db)) -> GetPagesService:
    """Get pages query service instance."""
    return GetPagesService(get_page_repository(db))

