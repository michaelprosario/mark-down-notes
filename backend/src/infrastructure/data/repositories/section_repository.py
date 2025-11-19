"""Section repository implementation."""

from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.domain.section import Section
from src.core.interfaces.repositories import ISectionRepository
from src.infrastructure.data.models.section_model import SectionModel


class SectionRepository(ISectionRepository):
    """Concrete implementation of section repository."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _to_domain(self, model: SectionModel) -> Section:
        """Convert ORM model to domain entity."""
        return Section(
            id=model.id,
            notebook_id=model.notebook_id,
            name=model.name,
            display_order=model.display_order,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
    
    def _to_model(self, entity: Section) -> SectionModel:
        """Convert domain entity to ORM model."""
        return SectionModel(
            id=entity.id,
            notebook_id=entity.notebook_id,
            name=entity.name,
            display_order=entity.display_order,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
    
    async def create(self, section: Section) -> Section:
        """Create a new section."""
        if not section.id:
            section.id = str(uuid.uuid4())
        
        model = self._to_model(section)
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        
        return self._to_domain(model)
    
    async def get_by_id(self, section_id: str) -> Optional[Section]:
        """Get section by ID."""
        query = select(SectionModel).where(SectionModel.id == section_id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        return self._to_domain(model) if model else None
    
    async def get_by_notebook_id(self, notebook_id: str, include_deleted: bool = False) -> List[Section]:
        """Get all sections in a notebook."""
        query = select(SectionModel).where(SectionModel.notebook_id == notebook_id)
        
        if not include_deleted:
            query = query.where(SectionModel.deleted_at.is_(None))
        
        query = query.order_by(SectionModel.display_order)
        result = await self.db.execute(query)
        models = result.scalars().all()
        
        return [self._to_domain(model) for model in models]
    
    async def update(self, section: Section) -> Section:
        """Update existing section."""
        query = select(SectionModel).where(SectionModel.id == section.id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Section not found: {section.id}")
        
        model.name = section.name
        model.display_order = section.display_order
        model.updated_at = datetime.utcnow()
        
        await self.db.flush()
        await self.db.refresh(model)
        
        return self._to_domain(model)
    
    async def delete(self, section_id: str) -> bool:
        """Soft delete section."""
        query = select(SectionModel).where(SectionModel.id == section_id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        model.soft_delete()
        await self.db.flush()
        
        return True
    
    async def restore(self, section_id: str) -> bool:
        """Restore soft-deleted section."""
        query = select(SectionModel).where(SectionModel.id == section_id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        model.restore()
        await self.db.flush()
        
        return True
    
    async def reorder(self, section_id: str, new_order: int) -> Section:
        """Update section display order."""
        query = select(SectionModel).where(SectionModel.id == section_id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Section not found: {section_id}")
        
        model.display_order = new_order
        model.updated_at = datetime.utcnow()
        
        await self.db.flush()
        await self.db.refresh(model)
        
        return self._to_domain(model)
