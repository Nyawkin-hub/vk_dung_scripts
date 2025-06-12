import asyncio
import aiohttp
from scripts.autopost import autopost_loop
from scripts.triggerbaff import main as triggerbaff_main
from shared.config import logger

async def main():
    """Start the main application loop."""
    async with aiohttp.ClientSession() as session:
        try:
            await asyncio.gather(autopost_loop(), triggerbaff_main())
        except asyncio.CancelledError:
            logger.info("Program cancelled")
            raise

if __name__ == "__main__":
    asyncio.run(main())