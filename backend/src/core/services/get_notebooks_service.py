"""Service for querying notebooks."""

from typing import List

from src.core.queries.queries import GetNotebooksQuery, GetNotebookByIdQuery
from src.core.common.result import Result
from src.core.domain.notebook import Notebook
from src.core.interfaces.repositories import INotebookRepository


class GetNotebooksService:
    """Service to handle notebook retrieval business logic."""
    
    def __init__(self, notebook_repository: INotebookRepository):
        """
        Initialize the service.
        
        Args:
            notebook_repository: Repository for notebook persistence.
        """
        self.notebook_repository = notebook_repository
    
    async def execute(self, query: GetNotebooksQuery) -> Result[List[Notebook]]:
        """
        Execute the get notebooks query.
        
        Args:
            query: The get notebooks query.
            
        Returns:
            Result containing list of notebooks or error information.
        """
        try:
            notebooks = await self.notebook_repository.get_all(
                include_deleted=query.include_deleted
            )
            return Result.ok(notebooks, f"Retrieved {len(notebooks)} notebooks")
        except Exception as e:
            return Result.fail(f"Failed to retrieve notebooks: {str(e)}")
    
    async def get_by_id(self, query: GetNotebookByIdQuery) -> Result[Notebook]:
        """
        Execute the get notebook by id query.
        
        Args:
            query: The get notebook by id query.
            
        Returns:
            Result containing the notebook or error information.
        """
        try:
            notebook = await self.notebook_repository.get_by_id(query.id)
            if not notebook:
                return Result.fail(f"Notebook with id {query.id} not found")
            return Result.ok(notebook, "Notebook retrieved successfully")
        except Exception as e:
            return Result.fail(f"Failed to retrieve notebook: {str(e)}")
