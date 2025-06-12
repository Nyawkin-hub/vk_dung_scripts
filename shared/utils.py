import asyncio
import aiohttp
from shared.config import logger, VK_TRIGGERBAFF_INTERVAL
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