"""Integration test for the complete API hierarchy."""

import httpx
import asyncio


async def test_full_hierarchy():
    """Test creating notebook -> section -> page hierarchy."""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # 1. Create notebook
        notebook_response = await client.post(
            f"{base_url}/api/notebooks/",
            json={
                "name": "Test Notebook",
                "description": "Integration test",
                "color": "#FF5733"
            }
        )
        assert notebook_response.status_code == 201
        notebook = notebook_response.json()
        print(f"✓ Created notebook: {notebook['id']}")
        
        # 2. Create section
        section_response = await client.post(
            f"{base_url}/api/sections/",
            json={
                "notebook_id": notebook["id"],
                "name": "Chapter 1",
                "display_order": 0
            }
        )
        assert section_response.status_code == 201
        section = section_response.json()
        print(f"✓ Created section: {section['id']}")
        
        # 3. Create page
        page_response = await client.post(
            f"{base_url}/api/pages/",
            json={
                "section_id": section["id"],
                "title": "Introduction",
                "content": "# Welcome\n\nThis is a **test** page.",
                "display_order": 0
            }
        )
        assert page_response.status_code == 201
        page = page_response.json()
        print(f"✓ Created page: {page['id']}")
        print(f"  - Title: {page['title']}")
        print(f"  - Content plain: {page['content_plain']}")
        
        # 4. Get page by ID
        get_response = await client.get(f"{base_url}/api/pages/{page['id']}")
        assert get_response.status_code == 200
        retrieved_page = get_response.json()
        print(f"✓ Retrieved page: {retrieved_page['title']}")
        
        # 5. Update page
        update_response = await client.put(
            f"{base_url}/api/pages/{page['id']}",
            json={
                "title": "Updated Introduction",
                "content": "# Updated\n\nThis content was **updated**."
            }
        )
        assert update_response.status_code == 200
        updated_page = update_response.json()
        print(f"✓ Updated page: {updated_page['title']}")
        
        # 6. List pages by section
        list_response = await client.get(
            f"{base_url}/api/pages/",
            params={"section_id": section["id"]}
        )
        assert list_response.status_code == 200
        pages = list_response.json()
        print(f"✓ Listed {len(pages)} page(s) in section")
        
        # 7. Delete page
        delete_response = await client.delete(f"{base_url}/api/pages/{page['id']}")
        assert delete_response.status_code == 204
        print(f"✓ Deleted page")
        
        print("\n✅ All tests passed!")


if __name__ == "__main__":
    asyncio.run(test_full_hierarchy())
