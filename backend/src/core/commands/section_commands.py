"""Command objects for section operations."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateSectionCommand:
    """Command to create a new section."""
    notebook_id: str
    name: str
    display_order: int = 0


@dataclass
class UpdateSectionCommand:
    """Command to update an existing section."""
    id: str
    name: Optional[str] = None
    display_order: Optional[int] = None


@dataclass
class DeleteSectionCommand:
    """Command to delete a section."""
    id: str


@dataclass
class ReorderSectionsCommand:
    """Command to reorder sections."""
    section_id: str
    new_order: int
