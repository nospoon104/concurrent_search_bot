import asyncio
import logging

import aiohttp
from aiogram import Bot

from search_bot.bootstrap import (
    create_dispatcher,
    create_search_service,
)
from search_bot.config import load_settings


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    settings = load_settings()
    bot = Bot(token=settings.bot_token)
    dispatcher = create_dispatcher()

    timeout = aiohttp.ClientTimeout(
        total=settings.http_timeout,
    )

    async with aiohttp.ClientSession(
        headers={
            "User-Agent": "ConcurrentSearchBot/0.1 (educational project)",
        },
        timeout=timeout,
    ) as session:
        search_service = create_search_service(
            session,
            settings,
        )

        await dispatcher.start_polling(
            bot,
            search_service=search_service,
            settings=settings,
        )


if __name__ == "__main__":
    asyncio.run(main())
