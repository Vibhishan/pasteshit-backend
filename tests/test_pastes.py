import pytest
from fastapi.testclient import TestClient

from main import app
from database import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """
    Setup and teardown the database for tests.
    Creates all tables before each test and drops them after.
    """
    # Setup - create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown - drop tables
    Base.metadata.drop_all(bind=engine)


def test_create_paste():
    """Test creating a new paste."""
    # Prepare test data
    data = {"content": "Test paste content"}
    
    # Send request
    response = client.post("/api/v1/pastes", json=data)
    
    # Check response
    assert response.status_code == 201
    assert "id" in response.json()
    assert "url" in response.json()
    
    # Store paste ID for retrieval test
    paste_id = response.json()["id"]
    
    # Test retrieval
    response = client.get(f"/api/v1/pastes/{paste_id}")
    assert response.status_code == 200
    assert response.json()["id"] == paste_id
    assert response.json()["content"] == data["content"]


def test_get_nonexistent_paste():
    """Test retrieving a nonexistent paste."""
    response = client.get("/api/v1/pastes/nonexistent")
    assert response.status_code == 404


def test_delete_paste():
    """Test deleting a paste."""
    # Create a paste first
    data = {"content": "Test paste for deletion"}
    response = client.post("/api/v1/pastes", json=data)
    paste_id = response.json()["id"]
    
    # Delete the paste
    response = client.delete(f"/api/v1/pastes/{paste_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get(f"/api/v1/pastes/{paste_id}")
    assert response.status_code == 404 