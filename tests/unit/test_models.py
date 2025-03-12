import pytest
from app.models import PlexCredentials, AuthResponse, ServerInfo

def test_plex_credentials():
    """Test PlexCredentials model"""
    credentials = PlexCredentials(username="test_user", password="test_pass")
    assert credentials.username == "test_user"
    assert credentials.password == "test_pass"
    
    # Test validation
    with pytest.raises(ValueError):
        PlexCredentials(username="", password="test_pass")
    
    with pytest.raises(ValueError):
        PlexCredentials(username="test_user", password="")

def test_auth_response():
    """Test AuthResponse model"""
    # Test with server_url
    response = AuthResponse(token="test_token", server_url="http://test.com")
    assert response.token == "test_token"
    assert response.server_url == "http://test.com"
    
    # Test without server_url
    response = AuthResponse(token="test_token")
    assert response.token == "test_token"
    assert response.server_url is None
    
    # Test validation
    with pytest.raises(ValueError):
        AuthResponse(token="")

def test_server_info():
    """Test ServerInfo model"""
    server_info = ServerInfo(
        machine_identifier="test-id",
        version="1.0.0",
        claimed=True,
        server_url="http://test.com"
    )
    
    assert server_info.machine_identifier == "test-id"
    assert server_info.version == "1.0.0"
    assert server_info.claimed is True
    assert server_info.server_url == "http://test.com"
    
    # Test validation
    with pytest.raises(ValueError):
        ServerInfo(
            machine_identifier="",  # Empty string should fail
            version="1.0.0",
            claimed=True,
            server_url="http://test.com"
        )
    
    with pytest.raises(ValueError):
        ServerInfo(
            machine_identifier="test-id",
            version="",  # Empty string should fail
            claimed=True,
            server_url="http://test.com"
        )
    
    with pytest.raises(ValueError):
        ServerInfo(
            machine_identifier="test-id",
            version="1.0.0",
            claimed=True,
            server_url=""  # Empty string should fail
        ) 