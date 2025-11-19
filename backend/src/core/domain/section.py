"""Section domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Section:
    """
    Section domain entity.
    
    Represents a mid-level organizational unit within a notebook.
    """
    
    id: str
    notebook_id: str
    name: str
    display_order: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate section data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate name
        if not self.name or not self.name.strip():
            return False, "Section name cannot be empty"
        
        if len(self.name) > 100:
            return False, "Section name cannot exceed 100 characters"
        
        # Validate display order
        if self.display_order < 0:
            return False, "Display order must be non-negative"
        
        # Validate notebook_id
        if not self.notebook_id:
            return False, "Section must belong to a notebook"
        
        return True, None
    
    def is_deleted(self) -> bool:
        """Check if section is soft-deleted."""
        return self.deleted_at is not None
    
    def soft_delete(self) -> None:
        """Mark section as deleted."""
        self.deleted_at = datetime.utcnow()
    
    def restore(self) -> None:
        """Restore soft-deleted section."""
        self.deleted_at = None
