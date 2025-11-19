"""API router for page operations."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from src.api.dependencies import (
    get_create_page_service,
    get_update_page_service,
    get_delete_page_service,
    get_get_pages_service
)
from src.api.schemas import PageCreate, PageUpdate, PageResponse
from src.core.commands.page_commands import (
    CreatePageCommand,
    UpdatePageCommand,
    DeletePageCommand
)
from src.core.queries.queries import GetPagesQuery, GetPageByIdQuery
from src.core.services.create_page_service import CreatePageService
from src.core.services.update_page_service import UpdatePageService
from src.core.services.delete_page_service import DeletePageService
from src.core.services.get_pages_service import GetPagesService

router = APIRouter(
    prefix="/api/pages",
    tags=["pages"],
)


@router.get("/", response_model=List[PageResponse])
async def list_pages(
    section_id: Optional[str] = None,
    service: GetPagesService = Depends(get_get_pages_service),
):
    """
    List pages, optionally filtered by section.
    
    Args:
        section_id: Optional section UUID to filter by.
    
    Returns:
        List of pages.
    """
    query = GetPagesQuery(section_id=section_id, include_deleted=False)
    result = await service.execute(query)
    
    if not result.success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result.message)
    
    return [PageResponse(
        id=page.id,
        section_id=page.section_id,
        parent_page_id=page.parent_page_id,
        title=page.title,
        content=page.content,
        content_plain=page.content_plain,
        display_order=page.display_order,
        created_at=page.created_at,
        updated_at=page.updated_at,
        deleted_at=page.deleted_at
    ) for page in result.data]


@router.post("/", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
async def create_page(
    page_data: PageCreate,
    service: CreatePageService = Depends(get_create_page_service),
):
    """
    Create a new page in a section.
    
    Returns:
        Created page with ID.
    """
    command = CreatePageCommand(
        section_id=page_data.section_id,
        title=page_data.title,
        content=page_data.content,
        parent_page_id=page_data.parent_page_id,
        display_order=page_data.display_order
    )
    
    result = await service.execute(command)
    
    if not result.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)
    
    page = result.data
    return PageResponse(
        id=page.id,
        section_id=page.section_id,
        parent_page_id=page.parent_page_id,
        title=page.title,
        content=page.content,
        content_plain=page.content_plain,
        display_order=page.display_order,
        created_at=page.created_at,
        updated_at=page.updated_at,
        deleted_at=page.deleted_at
    )


@router.get("/{page_id}", response_model=PageResponse)
async def get_page(
    page_id: str,
    service: GetPagesService = Depends(get_get_pages_service),
):
    """
    Get page by ID.
    
    Args:
        page_id: UUID of the page.
    
    Returns:
        Page details with content.
    """
    query = GetPageByIdQuery(id=page_id)
    result = await service.get_by_id(query)
    
    if not result.success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.message)
    
    page = result.data
    return PageResponse(
        id=page.id,
        section_id=page.section_id,
        parent_page_id=page.parent_page_id,
        title=page.title,
        content=page.content,
        content_plain=page.content_plain,
        display_order=page.display_order,
        created_at=page.created_at,
        updated_at=page.updated_at,
        deleted_at=page.deleted_at
    )


@router.put("/{page_id}", response_model=PageResponse)
async def update_page(
    page_id: str,
    page_data: PageUpdate,
    service: UpdatePageService = Depends(get_update_page_service),
):
    """
    Update page content and metadata.
    
    Args:
        page_id: UUID of the page.
    
    Returns:
        Updated page.
    """
    command = UpdatePageCommand(
        id=page_id,
        title=page_data.title,
        content=page_data.content,
        display_order=page_data.display_order
    )
    
    result = await service.execute(command)
    
    if not result.success:
        if "not found" in result.message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)
    
    page = result.data
    return PageResponse(
        id=page.id,
        section_id=page.section_id,
        parent_page_id=page.parent_page_id,
        title=page.title,
        content=page.content,
        content_plain=page.content_plain,
        display_order=page.display_order,
        created_at=page.created_at,
        updated_at=page.updated_at,
        deleted_at=page.deleted_at
    )


@router.delete("/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_page(
    page_id: str,
    service: DeletePageService = Depends(get_delete_page_service),
):
    """
    Soft delete a page.
    
    Args:
        page_id: UUID of the page.
    
    Returns:
        Success confirmation.
    """
    command = DeletePageCommand(id=page_id)
    result = await service.execute(command)
    
    if not result.success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)
    
    return None


@router.post("/{page_id}/autosave", response_model=PageResponse)
async def autosave_page(
    page_id: str,
    page_data: PageUpdate,
    service: UpdatePageService = Depends(get_update_page_service),
):
    """
    Auto-save page content (debounced updates).
    
    Args:
        page_id: UUID of the page.
    
    Returns:
        Success confirmation with timestamp.
    """
    # For auto-save, use the same update logic
    command = UpdatePageCommand(
        id=page_id,
        title=page_data.title,
        content=page_data.content,
        display_order=page_data.display_order
    )
    
    result = await service.execute(command)
    
    if not result.success:
        if "not found" in result.message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result.message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)
    
    page = result.data
    return PageResponse(
        id=page.id,
        section_id=page.section_id,
        parent_page_id=page.parent_page_id,
        title=page.title,
        content=page.content,
        content_plain=page.content_plain,
        display_order=page.display_order,
        created_at=page.created_at,
        updated_at=page.updated_at,
        deleted_at=page.deleted_at
    )
