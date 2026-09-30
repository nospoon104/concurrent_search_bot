import asyncio
import os
import aiohttp
from dotenv import load_dotenv
from html import escape
from aiogram.enums import ParseMode

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message


from search_bot.models import SearchResult
from search_bot.search_service import SearchService
from search_bot.github import search_github
from search_bot.wikipedia import search_wikipedia
from search_bot.stackoverflow import search_stackoverflow
from search_bot.models import ProviderOutcome


router = Router()


def format_search_outcomes(outcomes: list[ProviderOutcome]) -> str:
    sections = []

    for outcome in outcomes:
        lines = [f"<b>{escape(outcome.source)}</b>"]

        if outcome.error is not None:
            lines.append(escape(outcome.error))
        elif not outcome.results:
            lines.append("Ничего не найдено.")
        else:
            for result in outcome.results:
                lines.append("")
                lines.append(escape(result.title))

                if result.description:
                    lines.append(escape(result.description))

                if result.details:
                    lines.append(escape(result.details))

                lines.append(escape(result.url))

        sections.append("\n".join(lines))

    return "\n\n".join(sections)


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет! Напиши запрос — поищу в Wikipedia, GitHub и Stack Overflow."
    )


@router.message()
async def handle_message(
    message: Message,
    search_service: SearchService,
) -> None:

    if message.text is None:
        await message.answer("Пока только текстовые сообщения")
        return

    query = message.text.strip()

    if not query:
        await message.answer("Нужен непустой поисковой запрос.")
        return

    outcomes = await search_service.search(query)

    await message.answer(
        format_search_outcomes(outcomes),
        parse_mode=ParseMode.HTML,
    )


async def main() -> None:
    load_dotenv()
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError("Токен не задан/не робит")

    bot = Bot(token=token)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    timeout = aiohttp.ClientTimeout(total=20)

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
            provider_timeout=20.0,
            max_concurrent_providers=3,
            search_timeout=30.0,
        )

        await dispatcher.start_polling(bot, search_service=search_service)


if __name__ == "__main__":
    asyncio.run(main())
