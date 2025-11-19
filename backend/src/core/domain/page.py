"""Page domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Page:
    """
    Page domain entity.
    
    Represents an individual note or document within a section.
    """
    
    id: str
    section_id: str
    title: str
    content: str = ""
    content_plain: str = ""
    parent_page_id: Optional[str] = None
    display_order: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate page data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate title
        if not self.title or not self.title.strip():
            return False, "Page title cannot be empty"
        
        if len(self.title) > 255:
            return False, "Page title cannot exceed 255 characters"
        
        # Validate section_id
        if not self.section_id:
            return False, "Page must belong to a section"
        
        # Validate display order
        if self.display_order < 0:
            return False, "Display order must be non-negative"
        
        return True, None
    
    def is_deleted(self) -> bool:
        """Check if page is soft-deleted."""
        return self.deleted_at is not None
    
    def soft_delete(self) -> None:
        """Mark page as deleted."""
        self.deleted_at = datetime.utcnow()
    
    def restore(self) -> None:
        """Restore soft-deleted page."""
        self.deleted_at = None
    
    def is_subpage(self) -> bool:
        """Check if this page is a subpage."""
        return self.parent_page_id is not None
