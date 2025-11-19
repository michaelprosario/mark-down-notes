"""Notebook repository implementation."""

from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.core.domain.notebook import Notebook
from src.core.interfaces.repositories import INotebookRepository
from src.infrastructure.data.models.notebook_model import NotebookModel


class NotebookRepository(INotebookRepository):
    """Concrete implementation of notebook repository."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _to_domain(self, model: NotebookModel) -> Notebook:
        """Convert ORM model to domain entity."""
        return Notebook(
            id=model.id,
            name=model.name,
            color=model.color,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
    
    def _to_model(self, entity: Notebook) -> NotebookModel:
        """Convert domain entity to ORM model."""
        return NotebookModel(
            id=entity.id,
            name=entity.name,
            color=entity.color,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
    
    async def create(self, notebook: Notebook) -> Notebook:
        """Create a new notebook."""
        if not notebook.id:
            notebook.id = str(uuid.uuid4())
        
        model = self._to_model(notebook)
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        
        return self._to_domain(model)
    
    async def get_by_id(self, notebook_id: str) -> Optional[Notebook]:
        """Get notebook by ID."""
        query = select(NotebookModel).where(NotebookModel.id == notebook_id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        return self._to_domain(model) if model else None
    
    async def get_all(self, include_deleted: bool = False) -> List[Notebook]:
        """Get all notebooks."""
        query = select(NotebookModel)
        
        if not include_deleted:
            query = query.where(NotebookModel.deleted_at.is_(None))
        
        query = query.order_by(NotebookModel.created_at.desc())
        result = await self.db.execute(query)
        models = result.scalars().all()
        
        return [self._to_domain(model) for model in models]
    
    async def update(self, notebook: Notebook) -> Notebook:
        """Update existing notebook."""
        query = select(NotebookModel).where(NotebookModel.id == notebook.id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Notebook not found: {notebook.id}")
        
        model.name = notebook.name
        model.color = notebook.color
        model.updated_at = datetime.utcnow()
        
        await self.db.flush()
        await self.db.refresh(model)
        
        return self._to_domain(model)
    
    async def delete(self, notebook_id: str) -> bool:
        """Soft delete notebook."""
        query = select(NotebookModel).where(NotebookModel.id == notebook_id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        model.soft_delete()
        await self.db.flush()
        
        return True
    
    async def restore(self, notebook_id: str) -> bool:
        """Restore soft-deleted notebook."""
        query = select(NotebookModel).where(NotebookModel.id == notebook_id)
        result = await self.db.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        model.restore()
        await self.db.flush()
        
        return True
