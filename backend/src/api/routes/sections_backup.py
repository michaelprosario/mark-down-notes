"""API router for section operations."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from src.api.dependencies import (
    get_create_section_service,
    get_update_section_service,
    get_delete_section_service,
    get_get_sections_service,
    get_reorder_sections_service
)
from src.api.schemas import SectionCreate, SectionUpdate, SectionResponse
from src.core.commands.section_commands import (
    CreateSectionCommand,
    UpdateSectionCommand,
    DeleteSectionCommand,
    ReorderSectionsCommand
)
from src.core.queries.queries import GetSectionsQuery, GetSectionByIdQuery
from src.core.services.create_section_service import CreateSectionService
from src.core.services.update_section_service import UpdateSectionService
from src.core.services.delete_section_service import DeleteSectionService
from src.core.services.get_sections_service import GetSectionsService
from src.core.services.reorder_sections_service import ReorderSectionsService

router = APIRouter(
    prefix="/api/sections",
    tags=["sections"],
)


@router.get("/", response_model=List[SectionResponse])
async def list_sections(
    notebook_id: Optional[str] = None,
    service: GetSectionsService = Depends(get_get_sections_service),
):
    """
    List sections, optionally filtered by notebook.
    
    Args:
        notebook_id: Optional notebook UUID to filter by.
    
    Returns:
        List of sections.
    """
    query = GetSectionsQuery(notebook_id=notebook_id, include_deleted=False)
    result = await service.execute(query)
    
    if not result.success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result.message)
    
    return [SectionResponse(
        id=section.id,
        notebook_id=section.notebook_id,
        name=section.name,
        display_order=section.display_order,
        created_at=section.created_at,
        updated_at=section.updated_at,
        deleted_at=section.deleted_at
    ) for section in result.data]


@router.post("/", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
async def create_section(
    section_data: SectionCreate,
    service: CreateSectionService = Depends(get_create_section_service),
):
    """
    Create a new section in a notebook.
    
    Returns:
        Created section with ID.
    """
    command = CreateSectionCommand(
        notebook_id=section_data.notebook_id,
        name=section_data.name,
        display_order=section_data.display_order
    )
    
    result = await service.execute(command)
    
    if not result.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)
    
    section = result.data
    return SectionResponse(
        id=section.id,
        notebook_id=section.notebook_id,
        name=section.name,
        display_order=section.display_order,
        created_at=section.created_at,
        updated_at=section.updated_at,
        deleted_at=section.deleted_at
    )


@router.get("/{section_id}", response_model=SectionResponse)
async def get_section(
    section_id: str,
    service: GetSectionsService = Depends(get_get_sections_service),
):
    """
    Get section by ID.
    
    Args:
        section_id: UUID of the section.
    
    Returns:
        Section details with pages.
    """
    query = GetSectionByIdQuery(id=section_id)
    result = await service.get_by_id(query)
    
    if not result.success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.message)
    
    section = result.data
    return SectionResponse(
        id=section.id,
        notebook_id=section.notebook_id,
        name=section.name,
        display_order=section.display_order,
        created_at=section.created_at,
        updated_at=section.updated_at,
        deleted_at=section.deleted_at
    )


@router.put("/{section_id}", response_model=SectionResponse)
async def update_section(
    section_id: str,
    section_data: SectionUpdate,
    service: UpdateSectionService = Depends(get_update_section_service),
):
    """
    Update section.
    
    Args:
        section_id: UUID of the section.
    
    Returns:
        Updated section.
    """
    command = UpdateSectionCommand(
        id=section_id,
        name=section_data.name,
        display_order=section_data.display_order
    )
    
    result = await service.execute(command)
    
    if not result.success:
        if "not found" in result.message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)
    
    section = result.data
    return SectionResponse(
        id=section.id,
        notebook_id=section.notebook_id,
        name=section.name,
        display_order=section.display_order,
        created_at=section.created_at,
        updated_at=section.updated_at,
        deleted_at=section.deleted_at
    )


@router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(
    section_id: str,
    service: DeleteSectionService = Depends(get_delete_section_service),
):
    """
    Soft delete a section.
    
    Args:
        section_id: UUID of the section.
    
    Returns:
        Success confirmation.
    """
    command = DeleteSectionCommand(id=section_id)
    result = await service.execute(command)
    
    if not result.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)
    
    return None


@router.put("/{section_id}/reorder", response_model=SectionResponse)
async def reorder_section(
    section_id: str,
    new_order: int,
    service: ReorderSectionsService = Depends(get_reorder_sections_service),
):
    """
    Update section display order.
    
    Args:
        section_id: UUID of the section.
        new_order: New display order value.
    
    Returns:
        Updated section with new order.
    """
    command = ReorderSectionsCommand(section_id=section_id, new_order=new_order)
    result = await service.execute(command)
    
    if not result.success:
        if "not found" in result.message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)
    
    section = result.data
    return SectionResponse(
        id=section.id,
        notebook_id=section.notebook_id,
        name=section.name,
        display_order=section.display_order,
        created_at=section.created_at,
        updated_at=section.updated_at,
        deleted_at=section.deleted_at
    )
