import asyncio
import time
import aiohttp

from shared.longpoll import long_poll_listener
from shared.vk_api import send_message
from shared.config import VK_AUTOPOST_PEER_ID, VK_AUTOPOST_MESSAGE, PEER_ID
from shared.triggers import load_triggers

triggers = load_triggers()
queue = asyncio.Queue()

async def message_sender(session):
    while True:
        msg = await queue.get()
        await send_message(session, msg['peer_id'], msg['text'], reply_to=msg['reply_to'])
        await asyncio.sleep(65)
        queue.task_done()

async def handle_message(session, peer_id, text, msg_id):
    if text in triggers:
        response = triggers[text]
        await queue.put({"peer_id": peer_id, "text": response, "reply_to": msg_id})

async def triggerbaff():
    async with aiohttp.ClientSession() as session:
        sender_task = asyncio.create_task(message_sender(session))
        await long_poll_listener(handle_message)

async def autopost():
    async with aiohttp.ClientSession() as session:
        while True:
            await send_message(session, VK_AUTOPOST_PEER_ID, VK_AUTOPOST_MESSAGE)
            await asyncio.sleep(11000)  # 10800 3 hours

async def main():
    # Запускаем оба таска параллельно
    await asyncio.gather(triggerbaff(), autopost())

if __name__ == "__main__":
    asyncio.run(main())
