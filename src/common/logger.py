import sys
from loguru import logger
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))  # Add project root to path
from src.common.config import settings

# Configure logger
logger.remove()  # Remove default handler
logger.add(
    sys.stdout,
    level=settings.log_level,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    backtrace=True,
    diagnose=True
)

def get_logger(name: str):
    """Get a configured logger instance for a module.
    
    Args:
        name (str): Name of the module (usually __name__)
        
    Returns:
        Logger: Configured logger instance
    """
    return logger.bind(module=name)