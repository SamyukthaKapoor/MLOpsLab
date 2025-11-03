from fastapi.testclient import TestClient
import sys
sys.path.insert(0, "src")

from main import app, items, next_id

client = TestClient(app)


def setup_function():
    """Reset storage before each test"""
    items.clear()
    # Reset next_id
    import main
    main.next_id = 1


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_item():
    """Test creating a new item"""
    response = client.post(
        "/items",
        json={"name": "Test Item", "description": "Test Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Item"
    assert data["description"] == "Test Description"


def test_create_multiple_items():
    """Test creating multiple items increments IDs"""
    response1 = client.post(
        "/items",
        json={"name": "Item 1", "description": "First item"}
    )
    response2 = client.post(
        "/items",
        json={"name": "Item 2", "description": "Second item"}
    )
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()["id"] == 1
    assert response2.json()["id"] == 2


def test_create_item_missing_fields():
    """Test creating item with missing required fields"""
    response = client.post(
        "/items",
        json={"name": "Only Name"}
    )
    assert response.status_code == 422


def test_read_items_empty():
    """Test reading items when none exist"""
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_read_items_with_data():
    """Test reading all items"""
    # Create some items
    client.post("/items", json={"name": "Item 1", "description": "Desc 1"})
    client.post("/items", json={"name": "Item 2", "description": "Desc 2"})
    
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Item 1"
    assert data[1]["name"] == "Item 2"


def test_read_single_item():
    """Test reading a specific item"""
    # Create an item
    create_response = client.post(
        "/items",
        json={"name": "Test Item", "description": "Test Desc"}
    )
    item_id = create_response.json()["id"]
    
    # Read it back
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Test Item"


def test_read_item_not_found():
    """Test reading non-existent item returns 404"""
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_update_item():
    """Test updating an existing item"""
    # Create an item
    create_response = client.post(
        "/items",
        json={"name": "Original", "description": "Original Desc"}
    )
    item_id = create_response.json()["id"]
    
    # Update it
    response = client.put(
        f"/items/{item_id}",
        json={"name": "Updated", "description": "Updated Desc"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["description"] == "Updated Desc"
    assert data["id"] == item_id


def test_update_item_not_found():
    """Test updating non-existent item returns 404"""
    response = client.put(
        "/items/999",
        json={"name": "Test", "description": "Test"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_update_item_missing_fields():
    """Test updating with missing fields fails validation"""
    # Create an item
    create_response = client.post(
        "/items",
        json={"name": "Test", "description": "Test"}
    )
    item_id = create_response.json()["id"]
    
    # Try to update with missing field
    response = client.put(
        f"/items/{item_id}",
        json={"name": "Only Name"}
    )
    assert response.status_code == 422


def test_delete_item():
    """Test deleting an item"""
    # Create an item
    create_response = client.post(
        "/items",
        json={"name": "To Delete", "description": "Will be deleted"}
    )
    item_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted"
    
    # Verify it's gone
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404


def test_delete_item_not_found():
    """Test deleting non-existent item returns 404"""
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_full_crud_workflow():
    """Test complete CRUD workflow"""
    # Create
    create_response = client.post(
        "/items",
        json={"name": "Workflow Item", "description": "Testing workflow"}
    )
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]
    
    # Read
    read_response = client.get(f"/items/{item_id}")
    assert read_response.status_code == 200
    assert read_response.json()["name"] == "Workflow Item"
    
    # Update
    update_response = client.put(
        f"/items/{item_id}",
        json={"name": "Updated Workflow", "description": "Updated"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Workflow"
    
    # Delete
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 200
    
    # Verify deletion
    final_read = client.get(f"/items/{item_id}")
    assert final_read.status_code == 404


def test_multiple_items_isolation():
    """Test that operations on one item don't affect others"""
    # Create multiple items
    item1 = client.post("/items", json={"name": "Item 1", "description": "Desc 1"})
    item2 = client.post("/items", json={"name": "Item 2", "description": "Desc 2"})
    item3 = client.post("/items", json={"name": "Item 3", "description": "Desc 3"})
    
    id1 = item1.json()["id"]
    id2 = item2.json()["id"]
    id3 = item3.json()["id"]
    
    # Delete middle item
    client.delete(f"/items/{id2}")
    
    # Verify others still exist
    assert client.get(f"/items/{id1}").status_code == 200
    assert client.get(f"/items/{id2}").status_code == 404
    assert client.get(f"/items/{id3}").status_code == 200
    
    # Update first item
    client.put(f"/items/{id1}", json={"name": "Updated 1", "description": "New"})
    
    # Verify third item unchanged
    item3_data = client.get(f"/items/{id3}").json()
    assert item3_data["name"] == "Item 3"
    assert item3_data["description"] == "Desc 3"

# failing a test on purpose

def test_update_item_not_found():
    """Test updating non-existent item returns 404"""
    response = client.put(
        "/items/999",
        json={"name": "Test", "description": "Test"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Item found"