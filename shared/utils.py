import asyncio
import aiohttp
import json
from shared.config import logger, VK_TRIGGERBAFF_INTERVAL, ITEMS_FILE
from shared.vk_api import send_message

async def message_sender(session: aiohttp.ClientSession, queue: asyncio.Queue):
    """message_sender is an asynchronous function that continuously sends messages from a queue."""
    while True:
        msg = await queue.get()
        try:
            await send_message(
                session,
                msg['peer_id'],
                msg['text'],
                reply_to=msg.get('reply_to')
            )
            logger.info(f"Msg send to peer_id={msg['peer_id']}: {msg['text']}")
        except Exception as e:
            logger.error(f"Error while send msg: {e}")
        await asyncio.sleep(VK_TRIGGERBAFF_INTERVAL) # Adjusted to TRIGGERBAFF_INTERVAL
        queue.task_done()

# items.json loading and formatting functions
def load_items() -> dict[str, int]:
    """Loads items and their prices from items.json"""
    try:
        with open(ITEMS_FILE, 'r', encoding='utf-8') as f:
            items = json.load(f)
        logger.info("Things loaded from items.json")
        return items
    except Exception as e:
        logger.error(f"Download error items.json: {e}")
        return {}

# formatting function for autopost messages
def format_autopost_message(items: dict[str, int]) -> str:
    """formats the autopost message from items and their prices"""
    lines = [f"Ты мне {item} - Я тебе {price}🌕" for item, price in items.items()]
    return "\n".join(lines)