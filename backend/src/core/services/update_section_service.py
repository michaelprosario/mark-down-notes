"""Service for updating sections."""

from src.core.commands.section_commands import UpdateSectionCommand
from src.core.common.result import Result
from src.core.domain.section import Section
from src.core.interfaces.repositories import ISectionRepository


class UpdateSectionService:
    """Service to handle section update business logic."""
    
    def __init__(self, section_repository: ISectionRepository):
        """
        Initialize the service.
        
        Args:
            section_repository: Repository for section persistence.
        """
        self.section_repository = section_repository
    
    async def execute(self, command: UpdateSectionCommand) -> Result[Section]:
        """
        Execute the update section command.
        
        Args:
            command: The update section command.
            
        Returns:
            Result containing the updated section or error information.
        """
        # Retrieve existing section
        section = await self.section_repository.get_by_id(command.id)
        if not section:
            return Result.fail(f"Section with id {command.id} not found")
        
        # Update fields
        if command.name is not None:
            section.name = command.name.strip()
        if command.display_order is not None:
            section.display_order = command.display_order
        
        # Validate domain rules
        is_valid, error_msg = section.validate()
        if not is_valid:
            return Result.fail(f"Validation failed: {error_msg}")
        
        # Persist
        try:
            updated_section = await self.section_repository.update(section)
            return Result.ok(updated_section, "Section updated successfully")
        except Exception as e:
            return Result.fail(f"Failed to update section: {str(e)}")
