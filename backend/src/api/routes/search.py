"""API router for search operations."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import get_db

router = APIRouter(
    prefix="/api/search",
    tags=["search"],
)


@router.get("/")
async def search_pages(
    q: str = "",
    db: AsyncSession = Depends(get_db),
):
    """
    Full-text search across pages.
    
    Args:
        q: Search query string.
    
    Returns:
        List of matching pages with highlights.
    """
    # TODO: Implement in Phase 6 (User Story 4)
    return {"results": [], "query": q}


@router.get("/suggest")
async def search_suggestions(
    q: str = "",
    db: AsyncSession = Depends(get_db),
):
    """
    Get search suggestions/autocomplete.
    
    Args:
        q: Partial search query.
    
    Returns:
        List of suggested completions.
    """
    # TODO: Implement in Phase 6 (User Story 4)
    return {"suggestions": [], "query": q}
