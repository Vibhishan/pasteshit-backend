import pytest
from fastapi import status

from app.core.config import get_settings

# Get settings
settings = get_settings()

def test_create_paste(client):
    """Test creating a new paste."""
    # Prepare test data
    data = {"content": "Test paste content"}
    
    # Send request
    response = client.post(f"{settings.API_V1_PREFIX}/pastes", json=data)
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert "url" in response.json()
    
    # Store paste ID for retrieval test
    paste_id = response.json()["id"]
    
    # Test retrieval
    response = client.get(f"{settings.API_V1_PREFIX}/pastes/{paste_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == paste_id
    assert response.json()["content"] == data["content"]


def test_get_nonexistent_paste(client):
    """Test retrieving a nonexistent paste."""
    response = client.get(f"{settings.API_V1_PREFIX}/pastes/nonexistent")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_paste(client):
    """Test deleting a paste."""
    # Create a paste first
    data = {"content": "Test paste for deletion"}
    response = client.post(f"{settings.API_V1_PREFIX}/pastes", json=data)
    paste_id = response.json()["id"]
    
    # Delete the paste
    response = client.delete(f"{settings.API_V1_PREFIX}/pastes/{paste_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's gone
    response = client.get(f"{settings.API_V1_PREFIX}/pastes/{paste_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND 