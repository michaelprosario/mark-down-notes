"""Service for deleting notebooks."""

from src.core.commands.notebook_commands import DeleteNotebookCommand
from src.core.common.result import Result
from src.core.interfaces.repositories import INotebookRepository


class DeleteNotebookService:
    """Service to handle notebook deletion business logic."""
    
    def __init__(self, notebook_repository: INotebookRepository):
        """
        Initialize the service.
        
        Args:
            notebook_repository: Repository for notebook persistence.
        """
        self.notebook_repository = notebook_repository
    
    async def execute(self, command: DeleteNotebookCommand) -> Result[bool]:
        """
        Execute the delete notebook command.
        
        Args:
            command: The delete notebook command.
            
        Returns:
            Result indicating success or failure.
        """
        # Check if notebook exists
        notebook = await self.notebook_repository.get_by_id(command.id)
        if not notebook:
            return Result.fail(f"Notebook with id {command.id} not found")
        
        # Perform soft delete
        try:
            success = await self.notebook_repository.delete(command.id)
            if success:
                return Result.ok(True, "Notebook deleted successfully")
            else:
                return Result.fail("Failed to delete notebook")
        except Exception as e:
            return Result.fail(f"Failed to delete notebook: {str(e)}")
