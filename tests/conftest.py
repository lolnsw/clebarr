import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Import app after setting test config path
os.environ["PLEX_MANAGER_CONFIG"] = str(Path(__file__).parent / "config/config.yaml")
from app.main import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI application"""
    return TestClient(app)

@pytest.fixture
def mock_plex_response():
    """Mock successful Plex API response"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<MediaContainer machineIdentifier="test-id" version="1.0.0" claimed="1" />"""

@pytest.fixture
def mock_libraries_response():
    """Mock successful libraries response"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<MediaContainer>
    <Directory key="1" title="Movies" type="movie" agent="com.plexapp.agents.themoviedb" scanner="Plex Movie Scanner" language="en" uuid="com.plexapp.agents.themoviedb://123456" updatedAt="2024-03-20T12:00:00Z" createdAt="2024-01-01T00:00:00Z" scannedAt="2024-03-20T12:00:00Z" />
    <Directory key="2" title="TV Shows" type="show" agent="com.plexapp.agents.thetvdb" scanner="Plex TV Series Scanner" language="en" uuid="com.plexapp.agents.thetvdb://789012" updatedAt="2024-03-20T12:00:00Z" createdAt="2024-01-01T00:00:00Z" scannedAt="2024-03-20T12:00:00Z" />
</MediaContainer>"""

@pytest.fixture
def valid_token():
    """Valid Plex token for testing"""
    return "valid-test-token" 