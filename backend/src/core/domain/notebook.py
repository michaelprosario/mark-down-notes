"""Notebook domain entity."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re


@dataclass
class Notebook:
    """
    Notebook domain entity.
    
    Represents a top-level organizational container for notes.
    """
    
    id: str
    name: str
    color: str = "#0078D4"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate notebook data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate name
        if not self.name or not self.name.strip():
            return False, "Notebook name cannot be empty"
        
        if len(self.name) > 100:
            return False, "Notebook name cannot exceed 100 characters"
        
        # Validate color format
        if self.color and not re.match(r'^#[0-9A-Fa-f]{6}$', self.color):
            return False, "Color must be a valid hex color (#RRGGBB)"
        
        return True, None
    
    def is_deleted(self) -> bool:
        """Check if notebook is soft-deleted."""
        return self.deleted_at is not None
    
    def soft_delete(self) -> None:
        """Mark notebook as deleted."""
        self.deleted_at = datetime.utcnow()
    
    def restore(self) -> None:
        """Restore soft-deleted notebook."""
        self.deleted_at = None
