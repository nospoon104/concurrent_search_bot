import asyncio
import os
import aiohttp

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message


from search_bot.models import SearchResult
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
async def handle_message(message: Message, session: aiohttp.ClientSession) -> None:
    if message.text is None:
        await message.answer("Пока только текстовые сообщения")
        return

    query = message.text.strip()

    if not query:
        await message.answer("Нужен непустой поисковой запрос.")
        return

    for heading, search in (
        ("Wikipedia", search_wikipedia),
        ("GitHub", search_github),
        ("Stack Overflow", search_stackoverflow),
    ):
        try:
            results = await search(session, query)
        except aiohttp.ClientResponseError as exc:
            print(f"{heading} HTTP error: status={exc.status}", flush=True)
            await message.answer(f"{heading}: ошибка HTTP {exc.status}.")
            continue
        except TimeoutError:
            print(f"{heading} request timed out", flush=True)
            await message.answer(f"{heading}: не ответил вовремя.")
            continue
        except aiohttp.ClientError as exc:
            print(f"{heading} network error: {type(exc).__name__}", flush=True)
            await message.answer(f"{heading}: не удалось соединиться.")
            continue

        if not results:
            await message.answer(f"{heading}: ничего не найдено.")
            continue

        await message.answer(format_results(results, heading))


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
        await dispatcher.start_polling(bot, session=session)


if __name__ == "__main__":
    asyncio.run(main())
