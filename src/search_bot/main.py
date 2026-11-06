import asyncio
import aiohttp
import logging
from html import escape
from aiogram.enums import ParseMode

from aiogram import Bot, Dispatcher


from search_bot.models import SearchResult
from search_bot.search_service import SearchService
from search_bot.github import search_github
from search_bot.wikipedia import search_wikipedia
from search_bot.stackoverflow import search_stackoverflow
from search_bot.models import ProviderOutcome
from search_bot.config import load_settings
from search_bot.handlers.search import router


async def main() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    settings = load_settings()

    bot = Bot(token=settings.bot_token)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    timeout = aiohttp.ClientTimeout(
        total=settings.http_timeout,
    )

    async with aiohttp.ClientSession(
        headers={"User-Agent": "ConcurrentSearchBot/0.1 (educational project)"},
        timeout=timeout,
    ) as session:
        search_service = SearchService(
            session=session,
            providers=[
                ("Wikipedia", search_wikipedia),
                ("GitHub", search_github),
                ("Stack Overflow", search_stackoverflow),
            ],
            provider_timeout=settings.provider_timeout,
            max_concurrent_providers=settings.max_concurrent_providers,
            search_timeout=settings.search_timeout,
        )

        await dispatcher.start_polling(
            bot,
            search_service=search_service,
            settings=settings,
        )


if __name__ == "__main__":
    asyncio.run(main())
