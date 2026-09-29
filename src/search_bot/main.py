import asyncio
import os
import aiohttp
from time import perf_counter

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message


from search_bot.models import SearchResult
from search_bot.search_service import SearchService
from search_bot.github import search_github
from search_bot.wikipedia import search_wikipedia
from search_bot.stackoverflow import search_stackoverflow


router = Router()


def format_results(results: list[SearchResult], heading: str) -> str:
    lines = [f"Поиск по {heading} вернул:"]

    for result in results:
        lines.append("")
        lines.append(result.title)
        lines.append(result.description)

        if result.details:
            lines.append(result.details)

        lines.append(result.url)

    return "\n".join(lines)


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

    for outcome in outcomes:
        if outcome.error is not None:
            await message.answer(f"{outcome.source}: {outcome.error}")
            continue

        if not outcome.results:
            await message.answer(f"{outcome.source}: ничего не найдено.")
            continue

        await message.answer(format_results(outcome.results, outcome.source))


async def main() -> None:
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
        )

        await dispatcher.start_polling(bot, search_service=search_service)


if __name__ == "__main__":
    asyncio.run(main())
