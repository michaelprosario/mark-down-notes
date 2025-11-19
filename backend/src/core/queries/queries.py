"""Query objects for data retrieval operations."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class GetNotebooksQuery:
    """Query to get all notebooks."""
    include_deleted: bool = False


@dataclass
class GetNotebookByIdQuery:
    """Query to get a specific notebook."""
    id: str


@dataclass
class GetSectionsQuery:
    """Query to get sections, optionally filtered by notebook."""
    notebook_id: Optional[str] = None
    include_deleted: bool = False


@dataclass
class GetSectionByIdQuery:
    """Query to get a specific section."""
    id: str


@dataclass
class GetPagesQuery:
    """Query to get pages, optionally filtered by section."""
    section_id: Optional[str] = None
    parent_page_id: Optional[str] = None
    include_deleted: bool = False


@dataclass
class GetPageByIdQuery:
    """Query to get a specific page."""
    id: str
