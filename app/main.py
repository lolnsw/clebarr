import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import httpx
from .models import ServerInfo
from .config import Config
from .routers import server
from .logging import setup_logger

# Set up logger for the main application
logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Clebarr",
    description="A FastAPI-based Plex Media Server management application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# Include routers
app.include_router(server.router)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return {"status": "healthy"}

@app.get("/server/info", response_model=ServerInfo)
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
        "Accept": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            logger.debug(f"Making request to {config.plex_base_url}/identity")
            response = await client.get(
                f"{config.plex_base_url}/identity",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()["MediaContainer"]
                logger.info("Successfully retrieved server information")
                return ServerInfo(
                    machine_identifier=data["machineIdentifier"],
                    version=data["version"],
                    claimed=data["claimed"],
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
                    status_code=response.status_code,
                    detail="Failed to connect to Plex server"
                )
                
    except httpx.RequestError as e:
        logger.error(f"Request error while fetching server info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to Plex server: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while fetching server info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to Plex server"
        ) 