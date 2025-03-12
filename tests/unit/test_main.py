import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_get_server_info_missing_token():
    """Test server info endpoint without token"""
    response = client.get("/server/info")
    assert response.status_code == 401
    assert response.json()["detail"] == "X-Plex-Token header is required"

@pytest.mark.asyncio
async def test_get_server_info_success():
    """Test successful server info retrieval"""
    mock_response = '<?xml version="1.0" encoding="UTF-8"?>\n<MediaContainer machineIdentifier="test-id" version="1.0.0" claimed="1" />'
    
    mock_response_obj = MagicMock()
    mock_response_obj.status_code = 200
    mock_response_obj.text = mock_response
    
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.return_value = mock_response_obj
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.get(
            "/server/info",
            headers={"X-Plex-Token": "test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["machine_identifier"] == "test-id"
        assert data["version"] == "1.0.0"
        assert data["claimed"] is True
        assert data["server_url"] == "http://test-server:32400"

@pytest.mark.asyncio
async def test_get_server_info_invalid_token():
    """Test server info with invalid token"""
    mock_response_obj = MagicMock()
    mock_response_obj.status_code = 401
    
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.return_value = mock_response_obj
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.get(
            "/server/info",
            headers={"X-Plex-Token": "invalid-token"}
        )
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid Plex token"

@pytest.mark.asyncio
async def test_get_server_info_connection_error():
    """Test server info with connection error"""
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.side_effect = Exception("Connection error")
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        response = client.get(
            "/server/info",
            headers={"X-Plex-Token": "test-token"}
        )
        
        assert response.status_code == 500
        assert "Failed to process server info" in response.json()["detail"] 