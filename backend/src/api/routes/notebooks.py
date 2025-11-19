"""API router for notebook operations."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_db

router = APIRouter(
    prefix="/api/notebooks",
    tags=["notebooks"],
)


@router.get("/")
async def list_notebooks(
    db: AsyncSession = Depends(get_db),
):
    """
    List all notebooks.
    
    Returns:
        List of notebooks with basic information.
    """
    # TODO: Implement in Phase 3 (User Story 1)
    return {"notebooks": []}


@router.post("/")
async def create_notebook(
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new notebook.
    
    Returns:
        Created notebook with ID.
    """
    # TODO: Implement in Phase 3 (User Story 1)
    return {"message": "Not implemented yet"}


@router.get("/{notebook_id}")
async def get_notebook(
    notebook_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get notebook by ID.
    
    Args:
        notebook_id: UUID of the notebook.
    
    Returns:
        Notebook details with sections.
    """
    # TODO: Implement in Phase 3 (User Story 1)
    return {"message": "Not implemented yet"}


@router.put("/{notebook_id}")
async def update_notebook(
    notebook_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Update notebook details.
    
    Args:
        notebook_id: UUID of the notebook.
    
    Returns:
        Updated notebook.
    """
    # TODO: Implement in Phase 3 (User Story 1)
    return {"message": "Not implemented yet"}


@router.delete("/{notebook_id}")
async def delete_notebook(
    notebook_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Soft delete a notebook.
    
    Args:
        notebook_id: UUID of the notebook.
    
    Returns:
        Success confirmation.
    """
    # TODO: Implement in Phase 3 (User Story 1)
    return {"message": "Not implemented yet"}
