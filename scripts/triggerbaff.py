import asyncio
import aiohttp
from shared.longpoll import long_poll_listener
from shared.triggers import load_triggers
from shared.utils import message_sender
from shared.config import VK_AUTOBAFF_PEER_ID, logger

async def handle_message(session: aiohttp.ClientSession, peer_id: int, text: str, msg_id: int, queue: asyncio.Queue, triggers: dict):
    """Check for triggers in the message and add a response to the queue."""
    if text in triggers:
        response = triggers[text]
        await queue.put({"peer_id": peer_id, "text": response, "reply_to": msg_id})
        logger.info(f"Add anser on '{text}' in peer_id={peer_id}")

async def main():
    """Main function to start the triggerbaff listener."""
    triggers = load_triggers()
    if not triggers:
        logger.error("Triggers not found, triggerbaff will not start")
        return

    async with aiohttp.ClientSession() as session:
        queue = asyncio.Queue()
        sender_task = asyncio.create_task(message_sender(session, queue))
        try:
            await long_poll_listener(lambda s, p, t, m: handle_message(s, p, t, m, queue, triggers))
        except asyncio.CancelledError:
            sender_task.cancel()
            logger.info("Autopost loop cancelled")
            raise

if __name__ == "__main__":
    asyncio.run(main())