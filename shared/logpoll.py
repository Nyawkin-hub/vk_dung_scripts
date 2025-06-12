import asyncio
import aiohttp
from shared.config import PEER_ID
from shared.triggers import load_triggers
from shared.vk_api import get_long_poll_params, send_message

triggers = load_triggers()

async def message_sender(session, queue):
    while True:
        msg = await queue.get()
        await send_message(session, msg['peer_id'], msg['text'], reply_to=msg['reply_to'])
        await asyncio.sleep(61)
        queue.task_done()

async def long_poll_listener(handle_message):
    async with aiohttp.ClientSession() as session:
        lp = await get_long_poll_params(session)
        if lp is None:
            return

        server, key, ts = lp["server"], lp["key"], lp["ts"]
        queue = asyncio.Queue()
        asyncio.create_task(message_sender(session, queue))

        while True:
            try:
                async with session.get(
                    f"https://{server}",
                    params={"act": "a_check", "key": key, "ts": ts, "wait": 25, "mode": 2, "version": 3},
                    timeout=30
                ) as resp:
                    data = await resp.json()

                if "failed" in data:
                    lp = await get_long_poll_params(session)
                    if lp is None:
                        return
                    server, key, ts = lp["server"], lp["key"], lp["ts"]
                    continue

                ts = data["ts"]
                for update in data.get("updates", []):
                    if isinstance(update, list) and update[0] == 4:
                        peer_id = update[3]
                        text = update[5].lower().strip()
                        msg_id = update[1]

                        if peer_id == PEER_ID:
                            # вызываем функцию-обработчик
                            await handle_message(session, peer_id, text, msg_id)

            except Exception as e:
                print("Error Longpoll:", e)
                await asyncio.sleep(5)