import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("VK_TOKEN")
PEER_ID = int(os.getenv("VK_PEER_ID"))
API_VERSION = "5.131"
VK_AUTOPOST_PEER_ID = int(os.getenv("VK_AUTOPOST_PEER_ID"))
VK_AUTOPOST_MESSAGE = os.getenv("VK_AUTOPOST_MESSAGE")