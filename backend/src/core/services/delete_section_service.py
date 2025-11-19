"""Service for deleting sections."""

from src.core.commands.section_commands import DeleteSectionCommand
from src.core.common.result import Result
from src.core.interfaces.repositories import ISectionRepository, IPageRepository


class DeleteSectionService:
    """Service to handle section deletion business logic with cascade validation."""
    
    def __init__(
        self, 
        section_repository: ISectionRepository,
        page_repository: IPageRepository
    ):
        """
        Initialize the service.
        
        Args:
            section_repository: Repository for section persistence.
            page_repository: Repository for page persistence (for cascade checks).
        """
        self.section_repository = section_repository
        self.page_repository = page_repository
    
    async def execute(self, command: DeleteSectionCommand) -> Result[bool]:
        """
        Execute the delete section command with cascade validation.
        
        Args:
            command: The delete section command.
            
        Returns:
            Result indicating success or failure.
        """
        # Check if section exists
        section = await self.section_repository.get_by_id(command.id)
        if not section:
            return Result.fail(f"Section with id {command.id} not found")
        
        # Check for existing pages (cascade validation)
        pages = await self.page_repository.get_by_section_id(
            command.id, 
            include_deleted=False
        )
        if pages:
            return Result.fail(
                f"Cannot delete section: contains {len(pages)} active page(s). "
                "Please delete or move the pages first."
            )
        
        # Perform soft delete
        try:
            success = await self.section_repository.delete(command.id)
            if success:
                return Result.ok(True, "Section deleted successfully")
            else:
                return Result.fail("Failed to delete section")
        except Exception as e:
            return Result.fail(f"Failed to delete section: {str(e)}")
