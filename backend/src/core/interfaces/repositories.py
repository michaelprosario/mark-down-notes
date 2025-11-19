"""Repository interfaces for domain entities."""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.domain.notebook import Notebook
from src.core.domain.section import Section
from src.core.domain.page import Page


class INotebookRepository(ABC):
    """Interface for notebook repository."""
    
    @abstractmethod
    async def create(self, notebook: Notebook) -> Notebook:
        """Create a new notebook."""
        pass
    
    @abstractmethod
    async def get_by_id(self, notebook_id: str) -> Optional[Notebook]:
        """Get notebook by ID."""
        pass
    
    @abstractmethod
    async def get_all(self, include_deleted: bool = False) -> List[Notebook]:
        """Get all notebooks."""
        pass
    
    @abstractmethod
    async def update(self, notebook: Notebook) -> Notebook:
        """Update existing notebook."""
        pass
    
    @abstractmethod
    async def delete(self, notebook_id: str) -> bool:
        """Soft delete notebook."""
        pass
    
    @abstractmethod
    async def restore(self, notebook_id: str) -> bool:
        """Restore soft-deleted notebook."""
        pass


class ISectionRepository(ABC):
    """Interface for section repository."""
    
    @abstractmethod
    async def create(self, section: Section) -> Section:
        """Create a new section."""
        pass
    
    @abstractmethod
    async def get_by_id(self, section_id: str) -> Optional[Section]:
        """Get section by ID."""
        pass
    
    @abstractmethod
    async def get_by_notebook_id(self, notebook_id: str, include_deleted: bool = False) -> List[Section]:
        """Get all sections in a notebook."""
        pass
    
    @abstractmethod
    async def update(self, section: Section) -> Section:
        """Update existing section."""
        pass
    
    @abstractmethod
    async def delete(self, section_id: str) -> bool:
        """Soft delete section."""
        pass
    
    @abstractmethod
    async def restore(self, section_id: str) -> bool:
        """Restore soft-deleted section."""
        pass
    
    @abstractmethod
    async def reorder(self, section_id: str, new_order: int) -> Section:
        """Update section display order."""
        pass


class IPageRepository(ABC):
    """Interface for page repository."""
    
    @abstractmethod
    async def create(self, page: Page) -> Page:
        """Create a new page."""
        pass
    
    @abstractmethod
    async def get_by_id(self, page_id: str) -> Optional[Page]:
        """Get page by ID."""
        pass
    
    @abstractmethod
    async def get_by_section_id(self, section_id: str, include_deleted: bool = False) -> List[Page]:
        """Get all pages in a section."""
        pass
    
    @abstractmethod
    async def get_by_parent_id(self, parent_page_id: str, include_deleted: bool = False) -> List[Page]:
        """Get all subpages of a page."""
        pass
    
    @abstractmethod
    async def update(self, page: Page) -> Page:
        """Update existing page."""
        pass
    
    @abstractmethod
    async def delete(self, page_id: str) -> bool:
        """Soft delete page."""
        pass
    
    @abstractmethod
    async def restore(self, page_id: str) -> bool:
        """Restore soft-deleted page."""
        pass
