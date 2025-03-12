import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
import httpx
import xml.etree.ElementTree as ET

from ..models import ServerInfo, Library
from ..config import Config
from ..logging import setup_logger

# Set up logger for this module
logger = setup_logger(__name__)

# Initialize router
router = APIRouter(
    prefix="/server",
    tags=["server"],
    responses={404: {"description": "Not found"}}
)

# Initialize config with optional path from environment
config_path = os.getenv("PLEX_MANAGER_CONFIG")
config = Config(config_path)

# Define the X-Plex-Token header scheme
plex_token_header = APIKeyHeader(name="X-Plex-Token", auto_error=False)

async def verify_token(token: str = Depends(plex_token_header)):
    """Dependency to verify the Plex token"""
    if not token:
        logger.warning("Request received without X-Plex-Token header")
        raise HTTPException(
            status_code=401,
            detail="X-Plex-Token header is required"
        )
    return token

@router.get("/info", response_model=ServerInfo)
async def get_server_info(token: str = Depends(verify_token)):
    """
    Get Plex server information using the provided token.
    This verifies the token is valid and returns basic server information.
    """
    logger.info("Fetching server information")
    headers = {
        "X-Plex-Token": token,
        "X-Plex-Client-Identifier": config.plex_client_config["identifier"],
        "X-Plex-Product": config.plex_client_config["product"],
        "X-Plex-Version": config.plex_client_config["version"],
        "X-Plex-Device": config.plex_client_config["device"],
        "X-Plex-Device-Name": config.plex_client_config["device_name"],
        "Accept": "application/xml"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            logger.debug(f"Making request to {config.plex_base_url}/identity")
            response = await client.get(
                f"{config.plex_base_url}/identity",
                headers=headers
            )
            
            if response.status_code == 200:
                # Parse XML response
                logger.debug(f"Received XML response: {response.text}")
                root = ET.fromstring(response.text)
                logger.debug(f"XML root tag: {root.tag}")
                
                # The root element itself is the MediaContainer
                if root.tag != "MediaContainer":
                    logger.error("Invalid response format: Root element is not MediaContainer")
                    raise HTTPException(
                        status_code=500,
                        detail="Invalid response format from Plex server"
                    )
                
                logger.info("Successfully retrieved server information")
                return ServerInfo(
                    machine_identifier=root.get("machineIdentifier", ""),
                    version=root.get("version", ""),
                    claimed=root.get("claimed", "0") == "1",
                    server_url=config.plex_base_url
                )
            elif response.status_code == 401:
                logger.error("Invalid Plex token provided")
                raise HTTPException(
                    status_code=401,
                    detail="Invalid Plex token"
                )
            else:
                logger.error(f"Failed to get server info. Status code: {response.status_code}")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to get server info"
                )
                
    except httpx.RequestError as e:
        logger.error(f"Request error while fetching server info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process server info: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while fetching server info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process server info: {str(e)}"
        )

@router.get("/libraries", response_model=list[Library])
async def get_libraries(token: str = Depends(verify_token)):
    """
    Get a list of all libraries from the Plex server.
    """
    logger.info("Fetching library list")
    headers = {
        "X-Plex-Token": token,
        "X-Plex-Client-Identifier": config.plex_client_config["identifier"],
        "X-Plex-Product": config.plex_client_config["product"],
        "X-Plex-Version": config.plex_client_config["version"],
        "X-Plex-Device": config.plex_client_config["device"],
        "X-Plex-Device-Name": config.plex_client_config["device_name"],
        "Accept": "application/xml"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            logger.debug(f"Making request to {config.plex_base_url}/library/sections")
            response = await client.get(
                f"{config.plex_base_url}/library/sections",
                headers=headers
            )
            
            if response.status_code == 200:
                # Parse XML response
                root = ET.fromstring(response.text)
                
                # Find all Directory elements
                directories = root.findall(".//Directory")
                if not directories:
                    logger.warning("No libraries found in response")
                    return []
                
                libraries = []
                for directory in directories:
                    try:
                        library = Library(
                            key=str(directory.get("key", "")),
                            title=str(directory.get("title", "")),
                            type=str(directory.get("type", "")),
                            agent=str(directory.get("agent", "")),
                            scanner=str(directory.get("scanner", "")),
                            language=str(directory.get("language", "")),
                            uuid=str(directory.get("uuid", "")),
                            updated_at=str(directory.get("updatedAt", "")),
                            created_at=str(directory.get("createdAt", "")),
                            scanned_at=str(directory.get("scannedAt", ""))
                        )
                        libraries.append(library)
                    except Exception as e:
                        logger.error(f"Error processing library section: {str(e)}")
                        continue
                
                logger.info(f"Successfully retrieved {len(libraries)} libraries")
                return libraries
            elif response.status_code == 401:
                logger.error("Invalid Plex token provided")
                raise HTTPException(
                    status_code=401,
                    detail="Invalid Plex token"
                )
            else:
                error_detail = f"Failed to connect to Plex server (Status: {response.status_code})"
                try:
                    error_data = response.json()
                    if "MediaContainer" in error_data and "error" in error_data["MediaContainer"]:
                        error_detail = error_data["MediaContainer"]["error"]
                except:
                    pass
                logger.error(f"Failed to get libraries: {error_detail}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=error_detail
                )
                
    except httpx.RequestError as e:
        logger.error(f"Request error while fetching libraries: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to Plex server: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while fetching libraries: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process libraries: {str(e)}"
        ) 