import asyncio
import os
import aiohttp

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message


from search_bot.models import SearchResult
from search_bot.wikipedia import HEADERS, search_wikipedia


router = Router()


def format_wikipedia_results(results: list[SearchResult]) -> str:
    lines = ["В Wikipedia нашел вот это:"]

    for result in results:
        lines.extend(
            [
                "",
                result.title,
                result.description,
                result.url,
            ]
        )

    return "\n".join(lines)


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer("Привет! Отправь текстовый запрос — я пошукаю в Wikipedia")


@router.message()
async def handle_message(message: Message) -> None:
    if message.text is None:
        await message.answer("Пока только текстовые сообщения")
        return

    query = message.text.strip()

    if not query:
        await message.answer("Нужен непустой поисковой запрос.")
        return

    timeout = aiohttp.ClientTimeout(total=20)

    try:
        async with aiohttp.ClientSession(
            headers=HEADERS,
            timeout=timeout,
        ) as session:
            results = await search_wikipedia(session, query)
    except (aiohttp.ClientError, TimeoutError):
        await message.answer("Не удалось получить ответ Wikipedia. Попробуй позже.")
        return

    if not results:
        await message.answer("Wikipedia не нашла результатов по этому запросу.")
        return

    await message.answer(format_wikipedia_results(results))


async def main() -> None:
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError("Токен не задан/не робит")

    bot = Bot(token=token)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
