"""Service for updating notebooks."""

from src.core.commands.notebook_commands import UpdateNotebookCommand
from src.core.common.result import Result
from src.core.domain.notebook import Notebook
from src.core.interfaces.repositories import INotebookRepository


class UpdateNotebookService:
    """Service to handle notebook update business logic."""
    
    def __init__(self, notebook_repository: INotebookRepository):
        """
        Initialize the service.
        
        Args:
            notebook_repository: Repository for notebook persistence.
        """
        self.notebook_repository = notebook_repository
    
    async def execute(self, command: UpdateNotebookCommand) -> Result[Notebook]:
        """
        Execute the update notebook command.
        
        Args:
            command: The update notebook command.
            
        Returns:
            Result containing the updated notebook or error information.
        """
        # Retrieve existing notebook
        notebook = await self.notebook_repository.get_by_id(command.id)
        if not notebook:
            return Result.fail(f"Notebook with id {command.id} not found")
        
        # Update fields
        if command.name is not None:
            notebook.name = command.name.strip()
        if command.color is not None:
            notebook.color = command.color
        
        # Validate domain rules
        is_valid, error_msg = notebook.validate()
        if not is_valid:
            return Result.fail(f"Validation failed: {error_msg}")
        
        # Persist
        try:
            updated_notebook = await self.notebook_repository.update(notebook)
            return Result.ok(updated_notebook, "Notebook updated successfully")
        except Exception as e:
            return Result.fail(f"Failed to update notebook: {str(e)}")
