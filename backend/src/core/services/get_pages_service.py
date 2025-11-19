"""Service for querying pages."""

from typing import List

from src.core.queries.queries import GetPagesQuery, GetPageByIdQuery
from src.core.common.result import Result
from src.core.domain.page import Page
from src.core.interfaces.repositories import IPageRepository


class GetPagesService:
    """Service to handle page retrieval business logic."""
    
    def __init__(self, page_repository: IPageRepository):
        """
        Initialize the service.
        
        Args:
            page_repository: Repository for page persistence.
        """
        self.page_repository = page_repository
    
    async def execute(self, query: GetPagesQuery) -> Result[List[Page]]:
        """
        Execute the get pages query.
        
        Args:
            query: The get pages query.
            
        Returns:
            Result containing list of pages or error information.
        """
        try:
            if query.section_id:
                pages = await self.page_repository.get_by_section_id(
                    query.section_id,
                    include_deleted=query.include_deleted
                )
            elif query.parent_page_id:
                pages = await self.page_repository.get_by_parent_id(
                    query.parent_page_id,
                    include_deleted=query.include_deleted
                )
            else:
                pages = []
            return Result.ok(pages, f"Retrieved {len(pages)} pages")
        except Exception as e:
            return Result.fail(f"Failed to retrieve pages: {str(e)}")
    
    async def get_by_id(self, query: GetPageByIdQuery) -> Result[Page]:
        """
        Execute the get page by id query.
        
        Args:
            query: The get page by id query.
            
        Returns:
            Result containing the page or error information.
        """
        try:
            page = await self.page_repository.get_by_id(query.id)
            if not page:
                return Result.fail(f"Page with id {query.id} not found")
            return Result.ok(page, "Page retrieved successfully")
        except Exception as e:
            return Result.fail(f"Failed to retrieve page: {str(e)}")
