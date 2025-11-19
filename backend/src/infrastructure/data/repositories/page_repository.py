"""Page repository implementation."""

from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.domain.page import Page
from src.core.interfaces.repositories import IPageRepository
from src.infrastructure.data.models.page_model import PageModel


class PageRepository(IPageRepository):
    """Concrete implementation of page repository."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _to_domain(self, model: PageModel) -> Page:
        """Convert ORM model to domain entity."""
        return Page(
            id=model.id,
            section_id=model.section_id,
            title=model.title,
            content=model.content,
            content_plain=model.content_plain,
            parent_page_id=model.parent_page_id,
            display_order=model.display_order,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
    
    def _to_model(self, entity: Page) -> PageModel:
        """Convert domain entity to ORM model."""
        return PageModel(
            id=entity.id,
            section_id=entity.section_id,
            title=entity.title,
            content=entity.content,
            content_plain=entity.content_plain,
            parent_page_id=entity.parent_page_id,
            display_order=entity.display_order,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
    
    async def create(self, page: Page) -> Page:
        """Create a new page."""
        if not page.id:
            page.id = str(uuid.uuid4())
        
        model = self._to_model(page)
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        
        return self._to_domain(model)
    
    async def get_by_id(self, page_id: str) -> Optional[Page]:
        """Get page by ID."""
        query = select(PageModel).where(PageModel.id == page_id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        return self._to_domain(model) if model else None
    
    async def get_by_section_id(self, section_id: str, include_deleted: bool = False) -> List[Page]:
        """Get all pages in a section."""
        query = select(PageModel).where(PageModel.section_id == section_id)
        
        if not include_deleted:
            query = query.where(PageModel.deleted_at.is_(None))
        
        query = query.order_by(PageModel.display_order)
        result = await self.db.execute(query)
        models = result.scalars().all()
        
        return [self._to_domain(model) for model in models]
    
    async def get_by_parent_id(self, parent_page_id: str, include_deleted: bool = False) -> List[Page]:
        """Get all subpages of a page."""
        query = select(PageModel).where(PageModel.parent_page_id == parent_page_id)
        
        if not include_deleted:
            query = query.where(PageModel.deleted_at.is_(None))
        
        query = query.order_by(PageModel.display_order)
        result = await self.db.execute(query)
        models = result.scalars().all()
        
        return [self._to_domain(model) for model in models]
    
    async def update(self, page: Page) -> Page:
        """Update existing page."""
        query = select(PageModel).where(PageModel.id == page.id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Page not found: {page.id}")
        
        model.title = page.title
        model.content = page.content
        model.content_plain = page.content_plain
        model.display_order = page.display_order
        model.updated_at = datetime.utcnow()
        
        await self.db.flush()
        await self.db.refresh(model)
        
        return self._to_domain(model)
    
    async def delete(self, page_id: str) -> bool:
        """Soft delete page."""
        query = select(PageModel).where(PageModel.id == page_id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        model.soft_delete()
        await self.db.flush()
        
        return True
    
    async def restore(self, page_id: str) -> bool:
        """Restore soft-deleted page."""
        query = select(PageModel).where(PageModel.id == page_id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        model.restore()
        await self.db.flush()
        
        return True
