"""Service for querying sections."""

from typing import List

from src.core.queries.queries import GetSectionsQuery, GetSectionByIdQuery
from src.core.common.result import Result
from src.core.domain.section import Section
from src.core.interfaces.repositories import ISectionRepository


class GetSectionsService:
    """Service to handle section retrieval business logic."""
    
    def __init__(self, section_repository: ISectionRepository):
        """
        Initialize the service.
        
        Args:
            section_repository: Repository for section persistence.
        """
        self.section_repository = section_repository
    
    async def execute(self, query: GetSectionsQuery) -> Result[List[Section]]:
        """
        Execute the get sections query.
        
        Args:
            query: The get sections query.
            
        Returns:
            Result containing list of sections or error information.
        """
        try:
            if query.notebook_id:
                sections = await self.section_repository.get_by_notebook_id(
                    query.notebook_id,
                    include_deleted=query.include_deleted
                )
            else:
                sections = await self.section_repository.get_all(
                    include_deleted=query.include_deleted
                )
            return Result.ok(sections, f"Retrieved {len(sections)} sections")
        except Exception as e:
            return Result.fail(f"Failed to retrieve sections: {str(e)}")
    
    async def get_by_id(self, query: GetSectionByIdQuery) -> Result[Section]:
        """
        Execute the get section by id query.
        
        Args:
            query: The get section by id query.
            
        Returns:
            Result containing the section or error information.
        """
        try:
            section = await self.section_repository.get_by_id(query.id)
            if not section:
                return Result.fail(f"Section with id {query.id} not found")
            return Result.ok(section, "Section retrieved successfully")
        except Exception as e:
            return Result.fail(f"Failed to retrieve section: {str(e)}")
