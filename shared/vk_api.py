import random
import aiohttp
from shared.config import TOKEN, API_VERSION

async def get_long_poll_params(session):
    params = {"access_token": TOKEN, "v": API_VERSION, "need_pts": 1}
    async with session.get("https://api.vk.com/method/messages.getLongPollServer", params=params) as resp:
        data = await resp.json()
        return data.get("response")

async def send_message(session, peer_id, message, reply_to=None):
    params = {
        "access_token": TOKEN,
        "v": API_VERSION,
        "peer_id": peer_id,
        "message": message,
        "random_id": random.randint(1, 2**31)
    }
    if reply_to:
        params["reply_to"] = reply_to
    async with session.post("https://api.vk.com/method/messages.send", params=params) as resp:
        return await resp.json()
