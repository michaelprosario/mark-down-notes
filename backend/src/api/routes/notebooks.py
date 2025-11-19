"""API router for notebook operations."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.api.dependencies import (
    get_create_notebook_service,
    get_update_notebook_service,
    get_delete_notebook_service,
    get_get_notebooks_service
)
from src.api.schemas import NotebookCreate, NotebookUpdate, NotebookResponse
from src.core.commands.notebook_commands import (
    CreateNotebookCommand,
    UpdateNotebookCommand,
    DeleteNotebookCommand
)
from src.core.queries.queries import GetNotebooksQuery, GetNotebookByIdQuery
from src.core.services.create_notebook_service import CreateNotebookService
from src.core.services.update_notebook_service import UpdateNotebookService
from src.core.services.delete_notebook_service import DeleteNotebookService
from src.core.services.get_notebooks_service import GetNotebooksService

router = APIRouter(
    prefix="/api/notebooks",
    tags=["notebooks"],
)


@router.get("/", response_model=List[NotebookResponse])
async def list_notebooks(
    service: GetNotebooksService = Depends(get_get_notebooks_service),
):
    """
    List all notebooks.
    
    Returns:
        List of notebooks with basic information.
    """
    query = GetNotebooksQuery(include_deleted=False)
    result = await service.execute(query)
    
    if not result.success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result.message)
    
    return [NotebookResponse(
        id=nb.id,
        name=nb.name,
        color=nb.color,
        created_at=nb.created_at,
        updated_at=nb.updated_at,
        deleted_at=nb.deleted_at
    ) for nb in result.data]


@router.post("/", response_model=NotebookResponse, status_code=status.HTTP_201_CREATED)
async def create_notebook(
    notebook_data: NotebookCreate,
    service: CreateNotebookService = Depends(get_create_notebook_service),
):
    """
    Create a new notebook.
    
    Returns:
        Created notebook with ID.
    """
    command = CreateNotebookCommand(
        name=notebook_data.name,
        color=notebook_data.color
    )
    
    result = await service.execute(command)
    
    if not result.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)
    
    notebook = result.data
    return NotebookResponse(
        id=notebook.id,
        name=notebook.name,
        color=notebook.color,
        created_at=notebook.created_at,
        updated_at=notebook.updated_at,
        deleted_at=notebook.deleted_at
    )


@router.get("/{notebook_id}", response_model=NotebookResponse)
async def get_notebook(
    notebook_id: str,
    service: GetNotebooksService = Depends(get_get_notebooks_service),
):
    """
    Get notebook by ID.
    
    Args:
        notebook_id: UUID of the notebook.
    
    Returns:
        Notebook details with sections.
    """
    query = GetNotebookByIdQuery(id=notebook_id)
    result = await service.get_by_id(query)
    
    if not result.success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.message)
    
    notebook = result.data
    return NotebookResponse(
        id=notebook.id,
        name=notebook.name,
        color=notebook.color,
        created_at=notebook.created_at,
        updated_at=notebook.updated_at,
        deleted_at=notebook.deleted_at
    )


@router.put("/{notebook_id}", response_model=NotebookResponse)
async def update_notebook(
    notebook_id: str,
    notebook_data: NotebookUpdate,
    service: UpdateNotebookService = Depends(get_update_notebook_service),
):
    """
    Update notebook.
    
    Args:
        notebook_id: UUID of the notebook.
    
    Returns:
        Updated notebook.
    """
    command = UpdateNotebookCommand(
        id=notebook_id,
        name=notebook_data.name,
        color=notebook_data.color
    )
    
    result = await service.execute(command)
    
    if not result.success:
        if "not found" in result.message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)
    
    notebook = result.data
    return NotebookResponse(
        id=notebook.id,
        name=notebook.name,
        color=notebook.color,
        created_at=notebook.created_at,
        updated_at=notebook.updated_at,
        deleted_at=notebook.deleted_at
    )


@router.delete("/{notebook_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notebook(
    notebook_id: str,
    service: DeleteNotebookService = Depends(get_delete_notebook_service),
):
    """
    Soft delete a notebook.
    
    Args:
        notebook_id: UUID of the notebook.
    
    Returns:
        Success confirmation.
    """
    command = DeleteNotebookCommand(id=notebook_id)
    result = await service.execute(command)
    
    if not result.success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.message)
    
    return None

