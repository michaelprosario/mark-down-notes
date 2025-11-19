"""API router for section operations."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_db

router = APIRouter(
    prefix="/api/sections",
    tags=["sections"],
)


@router.get("/")
async def list_sections(
    notebook_id: str = None,
    db: AsyncSession = Depends(get_db),
):
    """
    List sections, optionally filtered by notebook.
    
    Args:
        notebook_id: Optional notebook UUID to filter by.
    
    Returns:
        List of sections.
    """
    # TODO: Implement in Phase 3 (User Story 1)
    return {"sections": []}


@router.post("/")
async def create_section(
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new section in a notebook.
    
    Returns:
        Created section with ID.
    """
    # TODO: Implement in Phase 3 (User Story 1)
    return {"message": "Not implemented yet"}


@router.get("/{section_id}")
async def get_section(
    section_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get section by ID.
    
    Args:
        section_id: UUID of the section.
    
    Returns:
        Section details with pages.
    """
    # TODO: Implement in Phase 3 (User Story 1)
    return {"message": "Not implemented yet"}


@router.put("/{section_id}")
async def update_section(
    section_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Update section details.
    
    Args:
        section_id: UUID of the section.
    
    Returns:
        Updated section.
    """
    # TODO: Implement in Phase 3 (User Story 1)
    return {"message": "Not implemented yet"}


@router.delete("/{section_id}")
async def delete_section(
    section_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Soft delete a section.
    
    Args:
        section_id: UUID of the section.
    
    Returns:
        Success confirmation.
    """
    # TODO: Implement in Phase 3 (User Story 1)
    return {"message": "Not implemented yet"}


@router.put("/{section_id}/reorder")
async def reorder_section(
    section_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Update section display order.
    
    Args:
        section_id: UUID of the section.
    
    Returns:
        Updated section with new order.
    """
    # TODO: Implement in Phase 3 (User Story 1)
    return {"message": "Not implemented yet"}
