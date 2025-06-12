import os
from shared.config import logger

def load_triggers() -> dict[str, str]:
    """Loads triggers from environment variables prefixed with 'TRIGGER_'."""
    triggers = {}
    for key, value in os.environ.items():
        if key.startswith("TRIGGER_"):
            trigger = key.replace("TRIGGER_", "").replace("_", " ").lower()
            triggers[trigger] = value
            logger.info(f"Loaded triggers: {trigger}")
    if not triggers:
        logger.warning("Triggers not found in environment variables")
    return triggers