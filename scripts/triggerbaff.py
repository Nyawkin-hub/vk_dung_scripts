import asyncio
import aiohttp
from shared.longpoll import long_poll_listener
from shared.triggers import load_triggers
from shared.vk_api import send_message
from shared.config import PEER_ID

triggers = load_triggers()
queue = asyncio.Queue()

async def message_sender(session):
    while True:
        msg = await queue.get()
        await send_message(session, msg['peer_id'], msg['text'], reply_to=msg['reply_to'])
        await asyncio.sleep(61)  # cooldown before next message
        queue.task_done()

async def handle_message(session, peer_id, text, msg_id):
    if text in triggers:
        response = triggers[text]
        await queue.put({"peer_id": peer_id, "text": response, "reply_to": msg_id})

async def main():
    async with aiohttp.ClientSession() as session:
        sender_task = asyncio.create_task(message_sender(session))
        await long_poll_listener(handle_message)

if __name__ == "__main__":
    asyncio.run(main())
