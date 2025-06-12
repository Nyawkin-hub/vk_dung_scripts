import asyncio
import aiohttp
from shared.config import VK_AUTOPOST_PEER_ID, VK_AUTOPOST_MESSAGE, VK_AUTOPOST_INTERVAL, logger
from shared.utils import load_items, format_autopost_message
from shared.vk_api import send_message

async def autopost_loop():
    """Send autopost messages at regular intervals"""
    # realizer for itemsautopost
    # items = load_items()
    # if not items:
    #     logger.error("Не удалось загрузить вещи. Автопост не будет работать.")
    #     return
    # message = format_autopost_message(items)
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                await send_message(session, VK_AUTOPOST_PEER_ID, VK_AUTOPOST_MESSAGE)
                logger.info(f"Msg {VK_AUTOPOST_MESSAGE} send in peer_id={VK_AUTOPOST_PEER_ID}")
            except Exception as e:
                logger.error(f"Error in autopost_loop: {e}")
            await asyncio.sleep(VK_AUTOPOST_INTERVAL)

async def main():
    """Main function to start the autopost loop"""
    try:
        await autopost_loop()
    except asyncio.CancelledError:
        logger.info("Autopost loop cancelled")
        raise

if __name__ == "__main__":
    asyncio.run(main())