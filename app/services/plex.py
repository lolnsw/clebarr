from typing import Dict
import httpx
from fastapi import HTTPException

from ..config import config

class PlexService:
    def __init__(self):
        self.base_url = config.plex_base_url
        self.client_headers = {
            "X-Plex-Client-Identifier": config.plex_client_config["identifier"],
            "X-Plex-Product": config.plex_client_config["product"],
            "X-Plex-Version": config.plex_client_config["version"],
            "X-Plex-Device": config.plex_client_config["device"],
            "X-Plex-Device-Name": config.plex_client_config["device_name"],
            "Accept": "application/json"
        }

    def get_headers(self, token: str) -> Dict[str, str]:
        """Get headers with authentication token"""
        return {
            **self.client_headers,
            "X-Plex-Token": token
        }

    async def get_server_identity(self, token: str) -> Dict:
        """Get Plex server identity information"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/identity",
                    headers=self.get_headers(token)
                )
                
                if response.status_code == 200:
                    return response.json()["MediaContainer"]
                elif response.status_code == 401:
                    raise HTTPException(
                        status_code=401,
                        detail="Invalid Plex token"
                    )
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail="Failed to connect to Plex server"
                    )
                    
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to Plex server: {str(e)}"
            )

# Create a singleton instance
plex_service = PlexService() 