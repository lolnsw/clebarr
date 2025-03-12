import os
from pathlib import Path
from typing import Dict, Any
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    def __init__(self, config_path: str | Path | None = None):
        # Use provided config path or default to config/config.yaml
        self.config_path = Path(config_path) if config_path else Path("config/config.yaml")
        
        if not self.config_path.exists():
            raise FileNotFoundError(f"{self.config_path} not found")
            
        with open(self.config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        # Environment
        self.env = os.getenv("ENV", "development")
        
        # Plex server configuration
        self.plex_base_url = os.getenv("PLEX_SERVER_URL") or config_data["plex"]["server"]["base_url"]
        # Try to get token from environment variable first, fall back to config file
        self.plex_token = os.getenv("PLEX_TOKEN") or config_data["plex"]["server"].get("token")
        
        if not self.plex_token:
            raise ValueError("Plex token not found in environment variables or config file")
        
        # Plex client configuration
        self.plex_client_config: Dict[str, str] = config_data["plex"]["client"]
        
        # Logging configuration
        self.logging_config: Dict[str, Any] = config_data["logging"].copy()
        # Override log level from environment if set
        if os.getenv("LOG_LEVEL"):
            self.logging_config["level"] = os.getenv("LOG_LEVEL")
        
        # Create logs directory if it doesn't exist
        log_dir = Path(self.logging_config["file_path"]).parent
        log_dir.mkdir(parents=True, exist_ok=True)

# Create default config instance
config = Config() 