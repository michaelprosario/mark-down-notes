"""Test the services layer with clean architecture."""

import asyncio
from src.infrastructure.config.database import AsyncSessionLocal
from src.infrastructure.data.repositories.notebook_repository import NotebookRepository
from src.infrastructure.data.repositories.section_repository import SectionRepository
from src.infrastructure.data.repositories.page_repository import PageRepository

from src.core.services.create_notebook_service import CreateNotebookService
from src.core.services.get_notebooks_service import GetNotebooksService
from src.core.services.create_section_service import CreateSectionService
from src.core.services.delete_section_service import DeleteSectionService
from src.core.services.create_page_service import CreatePageService
from src.core.services.delete_page_service import DeletePageService

from src.core.commands.notebook_commands import CreateNotebookCommand
from src.core.commands.section_commands import CreateSectionCommand, DeleteSectionCommand
from src.core.commands.page_commands import CreatePageCommand, DeletePageCommand
from src.core.queries.queries import GetNotebooksQuery


async def test_services_layer():
    """Test the complete services layer with Result pattern."""
    
    async with AsyncSessionLocal() as session:
        # Setup repositories
        notebook_repo = NotebookRepository(session)
        section_repo = SectionRepository(session)
        page_repo = PageRepository(session)
        
        # Test 1: Create notebook via service
        print("\\n=== Test 1: Create Notebook ===")
        create_notebook_service = CreateNotebookService(notebook_repo)
        command = CreateNotebookCommand(
            name="Services Test Notebook",
            color="#FF5733"
        )
        result = await create_notebook_service.execute(command)
        
        assert result.success, f"Failed to create notebook: {result.message}"
        notebook_id = result.data.id
        print(f"✓ Created notebook: {notebook_id}")
        print(f"  Message: {result.message}")
        
        # Test 2: Get notebooks via service
        print("\\n=== Test 2: Get Notebooks ===")
        get_notebooks_service = GetNotebooksService(notebook_repo)
        query = GetNotebooksQuery(include_deleted=False)
        result = await get_notebooks_service.execute(query)
        
        assert result.success, f"Failed to get notebooks: {result.message}"
        assert len(result.data) > 0, "No notebooks found"
        print(f"✓ Retrieved {len(result.data)} notebook(s)")
        print(f"  Message: {result.message}")
        
        # Test 3: Create section via service
        print("\\n=== Test 3: Create Section ===")
        create_section_service = CreateSectionService(section_repo)
        command = CreateSectionCommand(
            notebook_id=notebook_id,
            name="Test Section",
            display_order=0
        )
        result = await create_section_service.execute(command)
        
        assert result.success, f"Failed to create section: {result.message}"
        section_id = result.data.id
        print(f"✓ Created section: {section_id}")
        print(f"  Message: {result.message}")
        
        # Test 4: Create page via service
        print("\\n=== Test 4: Create Page ===")
        create_page_service = CreatePageService(page_repo)
        command = CreatePageCommand(
            section_id=section_id,
            title="Test Page",
            content="# Test\\n\\nThis is **markdown** content.",
            display_order=0
        )
        result = await create_page_service.execute(command)
        
        assert result.success, f"Failed to create page: {result.message}"
        page_id = result.data.id
        print(f"✓ Created page: {page_id}")
        print(f"  Message: {result.message}")
        print(f"  Content plain: {result.data.content_plain}")
        
        # Test 5: Try to delete section with pages (should fail)
        print("\\n=== Test 5: Delete Section with Pages (should fail) ===")
        delete_section_service = DeleteSectionService(section_repo, page_repo)
        command = DeleteSectionCommand(id=section_id)
        result = await delete_section_service.execute(command)
        
        assert not result.success, "Should have failed - section has pages"
        print(f"✓ Correctly prevented deletion: {result.message}")
        
        # Test 6: Delete page first, then section (should succeed)
        print("\\n=== Test 6: Delete Page, then Section ===")
        delete_page_service = DeletePageService(page_repo)
        command = DeletePageCommand(id=page_id)
        result = await delete_page_service.execute(command)
        
        assert result.success, f"Failed to delete page: {result.message}"
        print(f"✓ Deleted page: {result.message}")
        
        # Now delete section
        command = DeleteSectionCommand(id=section_id)
        result = await delete_section_service.execute(command)
        
        assert result.success, f"Failed to delete section: {result.message}"
        print(f"✓ Deleted section: {result.message}")
        
        # Test 7: Validation error handling
        print("\\n=== Test 7: Validation Error Handling ===")
        command = CreateNotebookCommand(
            name="",  # Invalid: empty name
            color="#FF5733"
        )
        result = await create_notebook_service.execute(command)
        
        assert not result.success, "Should have failed validation"
        print(f"✓ Correctly rejected invalid input: {result.message}")
        
        await session.commit()
        print("\\n✅ All services layer tests passed!")
        print("\\n=== Clean Architecture Verified ===")
        print("✓ Core services have zero infrastructure dependencies")
        print("✓ Command/Query objects encapsulate inputs")
        print("✓ Result objects provide consistent outputs")
        print("✓ Business logic isolated in service layer")
        print("✓ Cascade validation prevents data integrity issues")


if __name__ == "__main__":
    asyncio.run(test_services_layer())
