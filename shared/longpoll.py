import asyncio
import aiohttp
from shared.config import VK_AUTOBAFF_PEER_ID, logger, VK_API_VERSION
from shared.vk_api import get_long_poll_params

async def long_poll_listener(handle_message):
    """Listen Long Poll and send msg in handle_message."""
    async with aiohttp.ClientSession() as session:
        lp = await get_long_poll_params(session)
        if lp is None:
            logger.error("Could not get Long Poll parameters")
            return

        server, key, ts = lp["server"], lp["key"], lp["ts"]
        backoff = 1  # boop

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
                        logger.error("Could not refresh Long Poll parameters")
                        return
                    server, key, ts = lp["server"], lp["key"], lp["ts"]
                    backoff = min(backoff * 2, 60)  # max backoff to 60 seconds
                    await asyncio.sleep(backoff)
                    continue

                backoff = 1  # boop
                ts = data["ts"]
                for update in data.get("updates", []):
                    if isinstance(update, list) and update[0] == 4:
                        peer_id = update[3]
                        text = update[5].lower().strip()
                        msg_id = update[1]
                        if peer_id == VK_AUTOBAFF_PEER_ID:
                            await handle_message(session, peer_id, text, msg_id)

            except Exception as e:
                logger.error(f"Error in Long Poll: {e}")
                backoff = min(backoff * 2, 60)
                await asyncio.sleep(backoff)