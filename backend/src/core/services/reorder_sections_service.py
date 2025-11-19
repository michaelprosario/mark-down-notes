"""Service for reordering sections."""

from src.core.commands.section_commands import ReorderSectionsCommand
from src.core.common.result import Result
from src.core.domain.section import Section
from src.core.interfaces.repositories import ISectionRepository


class ReorderSectionsService:
    """Service to handle section reordering business logic."""
    
    def __init__(self, section_repository: ISectionRepository):
        """
        Initialize the service.
        
        Args:
            section_repository: Repository for section persistence.
        """
        self.section_repository = section_repository
    
    async def execute(self, command: ReorderSectionsCommand) -> Result[Section]:
        """
        Execute the reorder sections command.
        
        Args:
            command: The reorder sections command.
            
        Returns:
            Result containing the updated section or error information.
        """
        # Retrieve section
        section = await self.section_repository.get_by_id(command.section_id)
        if not section:
            return Result.fail(f"Section with id {command.section_id} not found")
        
        # Validate new order
        if command.new_order < 0:
            return Result.fail("Display order must be non-negative")
        
        # Update order
        section.display_order = command.new_order
        
        # Validate domain rules
        is_valid, error_msg = section.validate()
        if not is_valid:
            return Result.fail(f"Validation failed: {error_msg}")
        
        # Persist
        try:
            updated_section = await self.section_repository.update(section)
            return Result.ok(updated_section, "Section reordered successfully")
        except Exception as e:
            return Result.fail(f"Failed to reorder section: {str(e)}")
