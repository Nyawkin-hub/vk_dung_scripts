import asyncio
import aiohttp
import time
from shared.vk_api import send_message
from shared.config import VK_AUTOPOST_PEER_ID, VK_AUTOPOST_MESSAGE

async def autopost_loop():
    async with aiohttp.ClientSession() as session:
        while True:
            print("Отправка сообщения в", time.strftime("%X"))
            await send_message(session, VK_AUTOPOST_PEER_ID, VK_AUTOPOST_MESSAGE)
            print("Ждем 15 секунд")
            await asyncio.sleep(15)  # 3 hours (10800 seconds)

if __name__ == "__main__":
    print("=== Запуск автопоста ===")
    asyncio.run(autopost_loop())
