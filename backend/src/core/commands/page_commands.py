"""Command objects for page operations."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CreatePageCommand:
    """Command to create a new page."""
    section_id: str
    title: str
    content: str
    parent_page_id: Optional[str] = None
    display_order: int = 0


@dataclass
class UpdatePageCommand:
    """Command to update an existing page."""
    id: str
    title: Optional[str] = None
    content: Optional[str] = None
    display_order: Optional[int] = None


@dataclass
class DeletePageCommand:
    """Command to delete a page."""
    id: str
