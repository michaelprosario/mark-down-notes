"""Service for updating pages."""

import re

from src.core.commands.page_commands import UpdatePageCommand
from src.core.common.result import Result
from src.core.domain.page import Page
from src.core.interfaces.repositories import IPageRepository


def extract_plain_text(markdown_content: str) -> str:
    """Extract plain text from markdown for search indexing."""
    text = markdown_content
    text = re.sub(r'```[\s\S]*?```', '', text)  # Remove code blocks
    text = re.sub(r'`[^`]*`', '', text)  # Remove inline code
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # Remove links but keep text
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)  # Remove images
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)  # Remove headers
    text = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\1', text)  # Remove bold/italic
    return text.strip()


class UpdatePageService:
    """Service to handle page update business logic."""
    
    def __init__(self, page_repository: IPageRepository):
        """
        Initialize the service.
        
        Args:
            page_repository: Repository for page persistence.
        """
        self.page_repository = page_repository
    
    async def execute(self, command: UpdatePageCommand) -> Result[Page]:
        """
        Execute the update page command.
        
        Args:
            command: The update page command.
            
        Returns:
            Result containing the updated page or error information.
        """
        # Retrieve existing page
        page = await self.page_repository.get_by_id(command.id)
        if not page:
            return Result.fail(f"Page with id {command.id} not found")
        
        # Update fields
        if command.title is not None:
            page.title = command.title.strip()
        if command.content is not None:
            page.content = command.content
            page.content_plain = extract_plain_text(command.content)
        if command.display_order is not None:
            page.display_order = command.display_order
        
        # Validate domain rules
        is_valid, error_msg = page.validate()
        if not is_valid:
            return Result.fail(f"Validation failed: {error_msg}")
        
        # Persist
        try:
            updated_page = await self.page_repository.update(page)
            return Result.ok(updated_page, "Page updated successfully")
        except Exception as e:
            return Result.fail(f"Failed to update page: {str(e)}")
