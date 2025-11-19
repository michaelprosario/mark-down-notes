"""Command objects for notebook operations."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CreateNotebookCommand:
    """Command to create a new notebook."""
    name: str
    color: str = "#0078D4"


@dataclass
class UpdateNotebookCommand:
    """Command to update an existing notebook."""
    id: str
    name: Optional[str] = None
    color: Optional[str] = None


@dataclass
class DeleteNotebookCommand:
    """Command to delete a notebook."""
    id: str
