import asyncio
import aiohttp
import re
from shared.longpoll import long_poll_listener
from shared.utils import load_items, message_sender
from shared.config import VK_AUTOPOST_PEER_ID, CHECK_PEER_ID, WATCHER_BOT_ID, logger
from shared.vk_api import send_message

# its working only in VK_AUTOPOST_PEER_ID
async def handle_message(session: aiohttp.ClientSession, VK_AUTOPOST_PEER_ID: int, text: str, msg_id: int, queue: asyncio.Queue, items: dict):
    """Handle processes messages from the autopost chat."""
    # matching the message format "передать <item> - <quantity> штук"
    # TODO can be (r"передать\s+([а-яА-Я]+)\s+-\s+(\d+)\s", text.lower().strip()) 
    match = re.match(r"передать\s+([а-яА-Я]+)\s+-\s+(\d+)\s+штук", text.lower().strip()) 
    if match and VK_AUTOPOST_PEER_ID == VK_AUTOPOST_PEER_ID: # dont know why we need this condition
        item, quantity = match.groups()
        quantity = int(quantity)
        if item not in items:
            logger.warning(f"'{item}' not found in items.json")
            return
        # saving the request to the queue for further processing
        await queue.put({
            "VK_AUTOPOST_PEER_ID": VK_AUTOPOST_PEER_ID,
            "text": f"waiting accept: {quantity}*{item}",
            "reply_to": msg_id,
            "item": item,
            "quantity": quantity,
            "original_msg_id": msg_id
        })

# TODO can be {item} witout {quantity}-------------------------------------------------

        logger.info(f"Request detected: send {quantity}*{item} in VK_AUTOPOST_PEER_ID={VK_AUTOPOST_PEER_ID}")

async def handle_watcher_message(session: aiohttp.ClientSession, VK_AUTOPOST_PEER_ID: int, text: str, msg_id: int, queue: asyncio.Queue, items: dict, pending: dict):
    """Handles messages from the BOT and check chat """
    # check if the message is from the bot
    if VK_AUTOPOST_PEER_ID == VK_AUTOPOST_PEER_ID:

# TODO check if can be another msg}----------------------------------------------------

        match = re.match(r"👝(.+?)\s*\(.+?\),\s*получено:\s*(\d+)\*([а-яА-Я]+)\s*от\s*игрока\s*(.+?)!", text.strip())
        if match:
            receiver, quantity, item, sender = match.groups()
            quantity = int(quantity)
            if item not in items:
                logger.warning(f"Item '{item}' not found in items.json")
                return
            # save в pending for further processing

# TODO can be {item} witout {quantity}}------------------------------------------------

            pending[msg_id] = {"receiver": receiver, "sender": sender, "item": item, "quantity": quantity}
            logger.info(f"Received from BOT: {quantity}*{item} from {sender} for {receiver}")

    # check if the message is from the check chat
    if VK_AUTOPOST_PEER_ID == CHECK_PEER_ID:
        match = re.match(r"Получено:\s*(\d+)\*([а-яА-Я]+)\s*(.+?)!\s*=>\s*(.+)", text.strip())
        if match:
            quantity, item, sender, receiver = match.groups()
            quantity = int(quantity)
            if item not in items:
                logger.warning(f"Item '{item}' not found in items.json")
                return
            # Search for the pending request that matches the item, quantity, sender, and receiver
            for pending_msg_id, data in list(pending.items()):
                if (data["item"].lower() == item.lower() and 
                    data["quantity"] == quantity and 
                    data["sender"] == sender and 
                    data["receiver"] == receiver):
                    # Accept the payment and send confirmation
                    gold = items[item] * quantity
                    discounted_gold = int(gold * 0.9)  # 10% комиссия
                    await queue.put({
                        "VK_AUTOPOST_PEER_ID": VK_AUTOPOST_PEER_ID,
                        "text": f"передать {gold} золота",
                        "reply_to": pending[pending_msg_id]["original_msg_id"]
                    })
                    await queue.put({
                        "VK_AUTOPOST_PEER_ID": CHECK_PEER_ID,
                        "text": f"Получено: 🌕{discounted_gold}: {receiver} => {sender}"
                    })
                    logger.info(f"Payment validated: {gold} gold for {quantity}*{item}")
                    del pending[pending_msg_id]
                    break

async def main():
    """Main function for processing payment for things"""
    items = load_items()
    if not items:
        logger.error("Things are not loaded. Completion.")
        return

    async with aiohttp.ClientSession() as session:
        queue = asyncio.Queue()
        pending = {}  # to store pending requests
        sender_task = asyncio.create_task(message_sender(session, queue))
        try:
            await long_poll_listener(lambda s, p, t, m: handle_watcher_message(s, p, t, m, queue, items, pending) if p in [VK_AUTOPOST_PEER_ID, CHECK_PEER_ID] else handle_message(s, p, t, m, queue, items))
        except asyncio.CancelledError:
            sender_task.cancel()
            logger.info("Payment processing has been halted")
            raise

if __name__ == "__main__":
    asyncio.run(main())