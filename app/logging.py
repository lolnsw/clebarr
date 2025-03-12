import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from .config import config

def setup_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.
    
    Args:
        name: The name of the logger
        log_file: Optional specific log file path. If not provided, uses the default from config.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(config.logging_config["level"])
    
    # Create formatters
    formatter = logging.Formatter(
        fmt=config.logging_config["format"],
        datefmt=config.logging_config["date_format"]
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_path = log_file or config.logging_config["file_path"]
    file_handler = logging.handlers.RotatingFileHandler(
        file_path,
        maxBytes=config.logging_config["max_bytes"],
        backupCount=config.logging_config["backup_count"]
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger 