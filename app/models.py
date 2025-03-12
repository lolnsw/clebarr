from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union, List

class PlexCredentials(BaseModel):
    username: str
    password: str

    @field_validator('username', 'password')
    @classmethod
    def validate_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Field cannot be empty')
        return v

class AuthResponse(BaseModel):
    token: str
    server_url: Optional[str] = None

    @field_validator('token')
    @classmethod
    def validate_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Token cannot be empty')
        return v

class ServerInfo(BaseModel):
    """
    Represents Plex server information.
    """
    machine_identifier: str = Field(
        ...,
        description="Unique identifier for the Plex server"
    )
    version: str = Field(
        ...,
        description="Version of the Plex Media Server"
    )
    claimed: bool = Field(
        ...,
        description="Whether the server has been claimed by a Plex account"
    )
    server_url: str = Field(
        ...,
        description="Base URL of the Plex server"
    )

    @field_validator('machine_identifier', 'version', 'server_url')
    @classmethod
    def validate_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Field cannot be empty')
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "machine_identifier": "96f2fe7a78c9dc1f16a16bedbe90f98149be16b4",
                "version": "1.31.3.6868-28fc46b27",
                "claimed": True,
                "server_url": "http://localhost:32400"
            }
        }
    }

class Library(BaseModel):
    """
    Represents a Plex library.
    """
    key: str = Field(
        ...,
        description="Unique key for the library"
    )
    title: str = Field(
        ...,
        description="Display title of the library"
    )
    type: str = Field(
        ...,
        description="Type of library (e.g., 'movie', 'show', 'music')"
    )
    agent: str = Field(
        ...,
        description="Metadata agent used for the library"
    )
    scanner: str = Field(
        ...,
        description="Scanner used for the library"
    )
    language: str = Field(
        ...,
        description="Language setting for the library"
    )
    uuid: str = Field(
        ...,
        description="Unique identifier for the library"
    )
    updated_at: str = Field(
        ...,
        description="Last update timestamp"
    )
    created_at: str = Field(
        ...,
        description="Creation timestamp"
    )
    scanned_at: str = Field(
        ...,
        description="Last scan timestamp"
    )

    @field_validator('key', 'title', 'type', 'agent', 'scanner', 'language', 'uuid')
    @classmethod
    def validate_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Field cannot be empty')
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "key": "1",
                "title": "Movies",
                "type": "movie",
                "agent": "com.plexapp.agents.themoviedb",
                "scanner": "Plex Movie Scanner",
                "language": "en",
                "uuid": "com.plexapp.agents.themoviedb://123456",
                "updated_at": "2024-03-20T12:00:00Z",
                "created_at": "2024-01-01T00:00:00Z",
                "scanned_at": "2024-03-20T12:00:00Z"
            }
        }
    } 