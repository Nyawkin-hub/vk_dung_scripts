import asyncio
import aiohttp
import random
import os

from dotenv import load_dotenv

load_dotenv()  # listen .env

TOKEN = os.getenv("VK_TOKEN")
PEER_ID = int(os.getenv("VK_PEER_ID"))
API_VERSION = "5.131"
TRIGGERS = {}

for key, value in os.environ.items():
    if key.startswith("TRIGGER_"):
        trigger = key.replace("TRIGGER_", "").replace("_", " ").lower()
        TRIGGERS[trigger] = value

print("Loaded triggers:")
for k, v in TRIGGERS.items():
    print(f"{k!r} -> {v!r}")

async def get_long_poll_params(session):
    params = {"access_token": TOKEN, "v": API_VERSION, "need_pts": 1}
    async with session.get("https://api.vk.com/method/messages.getLongPollServer", params=params) as resp:
        data = await resp.json()
        if "response" in data:
            return data["response"]
        else:
            print("Error longpoll server:", data)
            return None

async def send_message(session, peer_id, message, reply_to=None):
    params = {
        "access_token": TOKEN,
        "v": API_VERSION,
        "peer_id": peer_id,
        "message": message,
        "random_id": random.randint(1, 2**31)
    }
    if reply_to is not None:
        params["reply_to"] = reply_to

    async with session.post("https://api.vk.com/method/messages.send", params=params) as resp:
        data = await resp.json()
        if "error" in data:
            print(f"Error of send msg: {data['error']['error_msg']}")
            return False
        else:
            print(f"Send msg reply to {reply_to}, id: {data['response']}")
            return True

async def message_sender(session, queue):
    while True:
        msg = await queue.get()
        await send_message(session, msg['peer_id'], msg['text'], reply_to=msg['reply_to'])
        await asyncio.sleep(61)  # Pause for 61 seconds to avoid hitting rate limits
        queue.task_done()

async def long_poll_listener():
    async with aiohttp.ClientSession() as session:
        lp = await get_long_poll_params(session)
        if lp is None:
            return

        server = lp["server"]
        key = lp["key"]
        ts = lp["ts"]

        print("Long poll server address:", server)

        queue = asyncio.Queue()
        asyncio.create_task(message_sender(session, queue))

        while True:
            params = {
                "act": "a_check",
                "key": key,
                "ts": ts,
                "wait": 25,
                "mode": 2,
                "version": 3
            }
            try:
                async with session.get(f"https://{server}", params=params, timeout=30) as resp:
                    data = await resp.json()

                if "failed" in data:
                    print("Long poll failed, updating parameters")
                    lp = await get_long_poll_params(session)
                    if lp is None:
                        print("Failed to get new long poll parameters, exiting")
                        return
                    server = lp["server"]
                    key = lp["key"]
                    ts = lp["ts"]
                    continue

                ts = data["ts"]

                for update in data.get("updates", []):
                    if isinstance(update, list) and update[0] == 4:
                        peer_id = update[3]
                        text = update[5].lower().strip()
                        msg_id = update[1]

                        if peer_id == PEER_ID:
                            print(f"New msg {PEER_ID}: {text}")

                            if text in TRIGGERS:
                                response = TRIGGERS[text]
                                print(f"Trigger add to queue: {response}")
                                await queue.put({"peer_id": peer_id, "text": response, "reply_to": msg_id})

            except Exception as e:
                print("Error Longpoll:", e)
                await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(long_poll_listener())