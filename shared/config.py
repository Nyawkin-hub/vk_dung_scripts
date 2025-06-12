import os
from dotenv import load_dotenv
import logging

load_dotenv()

# logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# validate environment variables
def validate_env_var(name: str, required: bool = True, is_int: bool = False) -> str | int | None:
    value = os.getenv(name)
    if required and value is None:
        logger.error(f"{name} is not set in the environment")
        raise ValueError(f"{name} is required")
    if value and is_int:
        try:
            return int(value)
        except ValueError:
            logger.error(f"{name} needs to be an integer")
            raise ValueError(f"{name} needs to be an integer")
    return value

# environment variables from .env file
TOKEN = validate_env_var("VK_TOKEN")
VK_AUTOBAFF_PEER_ID = validate_env_var("VK_AUTOBAFF_PEER_ID", is_int=True)
VK_AUTOPOST_PEER_ID = validate_env_var("VK_AUTOPOST_PEER_ID", is_int=True)
VK_AUTOPOST_MESSAGE = validate_env_var("VK_AUTOPOST_MESSAGE")
VK_API_VERSION = validate_env_var("VK_API_VERSION", required=False) or "5.131"
VK_AUTOPOST_INTERVAL = int(os.getenv("AUTOPOST_INTERVAL", 10800))  
VK_TRIGGERBAFF_INTERVAL = int(os.getenv("TRIGGERBAFF_INTERVAL", 65)) 

CHECK_PEER_ID = validate_env_var("CHECK_PEER_ID", is_int=True)
WATCHER_BOT_ID = validate_env_var("WATCHER_BOT_ID", is_int=True)
ITEMS_FILE = validate_env_var("ITEMS_FILE", required=False) or "items.json"