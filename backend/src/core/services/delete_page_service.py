"""Service for deleting pages."""

from src.core.commands.page_commands import DeletePageCommand
from src.core.common.result import Result
from src.core.interfaces.repositories import IPageRepository


class DeletePageService:
    """Service to handle page deletion business logic."""
    
    def __init__(self, page_repository: IPageRepository):
        """
        Initialize the service.
        
        Args:
            page_repository: Repository for page persistence.
        """
        self.page_repository = page_repository
    
    async def execute(self, command: DeletePageCommand) -> Result[bool]:
        """
        Execute the delete page command.
        
        Args:
            command: The delete page command.
            
        Returns:
            Result indicating success or failure.
        """
        # Check if page exists
        page = await self.page_repository.get_by_id(command.id)
        if not page:
            return Result.fail(f"Page with id {command.id} not found")
        
        # Check for child pages (subpages)
        child_pages = await self.page_repository.get_by_parent_id(
            command.id,
            include_deleted=False
        )
        if child_pages:
            return Result.fail(
                f"Cannot delete page: contains {len(child_pages)} subpage(s). "
                "Please delete or move the subpages first."
            )
        
        # Perform soft delete
        try:
            success = await self.page_repository.delete(command.id)
            if success:
                return Result.ok(True, "Page deleted successfully")
            else:
                return Result.fail("Failed to delete page")
        except Exception as e:
            return Result.fail(f"Failed to delete page: {str(e)}")
