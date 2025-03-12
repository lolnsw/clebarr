import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from app.routers.server import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_get_libraries_missing_token():
    """Test libraries endpoint without token"""
    response = client.get("/server/libraries")
    assert response.status_code == 401
    assert response.json()["detail"] == "X-Plex-Token header is required"

@pytest.mark.asyncio
async def test_get_libraries_success(mock_libraries_response):
    """Test successful libraries retrieval"""
    mock_response_obj = MagicMock()
    mock_response_obj.status_code = 200
    mock_response_obj.text = mock_libraries_response
    
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.return_value = mock_response_obj
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.get(
            "/server/libraries",
            headers={"X-Plex-Token": "test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["key"] == "1"
        assert data[0]["title"] == "Movies"
        assert data[0]["type"] == "movie"
        assert data[1]["key"] == "2"
        assert data[1]["title"] == "TV Shows"
        assert data[1]["type"] == "show"

@pytest.mark.asyncio
async def test_get_libraries_invalid_token():
    """Test libraries with invalid token"""
    mock_response_obj = MagicMock()
    mock_response_obj.status_code = 401
    
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.return_value = mock_response_obj
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.get(
            "/server/libraries",
            headers={"X-Plex-Token": "invalid-token"}
        )
        
        assert response.status_code == 401
        assert "Invalid Plex token" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_libraries_connection_error():
    """Test libraries with connection error"""
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.side_effect = Exception("Connection error")
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.get(
            "/server/libraries",
            headers={"X-Plex-Token": "test-token"}
        )
        
        assert response.status_code == 500
        assert "Failed to process libraries: Connection error" in response.json()["detail"] 