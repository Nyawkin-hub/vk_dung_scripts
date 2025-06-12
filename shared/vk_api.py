import uuid
import aiohttp
from shared.config import TOKEN, VK_API_VERSION, logger

async def get_long_poll_params(session: aiohttp.ClientSession) -> dict | None:
    """Take long poll parameters from VK API."""
    params = {"access_token": TOKEN, "v": VK_API_VERSION, "need_pts": 1}
    try:
        async with session.get("https://api.vk.com/method/messages.getLongPollServer", params=params) as resp:
            data = await resp.json()
            if "error" in data:
                logger.error(f"Erroe API in get_long_poll_params: {data['error']}")
                return None
            return data.get("response")
    except Exception as e:
        logger.error(f"Error in get_long_poll_params: {e}")
        return None

async def send_message(session: aiohttp.ClientSession, peer_id: int, message: str, reply_to: int | None = None) -> dict:
    """Send a message to a user or chat in VK."""
    params = {
        "access_token": TOKEN,
        "v": VK_API_VERSION,
        "peer_id": peer_id,
        "message": message,
        "random_id": int(uuid.uuid4().int & (2**31 - 1))  # unique random_id
    }
    if reply_to:
        params["reply_to"] = reply_to
    try:
        async with session.post("https://api.vk.com/method/messages.send", params=params) as resp:
            data = await resp.json()
            if "error" in data:
                logger.error(f"Error API in send_message: {data['error']}")
            return data
    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        return {"error": str(e)}