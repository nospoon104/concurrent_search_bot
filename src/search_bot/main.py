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
async def handle_message(message: Message, session: aiohttp.ClientSession) -> None:
    if message.text is None:
        await message.answer("Пока только текстовые сообщения")
        return

    query = message.text.strip()

    if not query:
        await message.answer("Нужен непустой поисковой запрос.")
        return

    try:
        results = await search_wikipedia(session, query)
    except aiohttp.ClientResponseError as exc:
        print(f"Wikipedia HTTP error: status={exc.status}", flush=True)

        if exc.status == 429:
            retry_after = (
                exc.headers.get("Retry-After") if exc.headers is not None else None
            )

            if retry_after is not None and retry_after.isdigit():
                text = (
                    "Wikipedia временно ограничила запросы. "
                    f"Попробуй не раньше чем через {retry_after} секунд."
                )
            else:
                text = "Wikipedia временно ограничила запросы. " "Попробуй позже."
        else:
            text = "Wikipedia вернула ошибку. Попробуй позже."

        await message.answer(text)
        return

    except TimeoutError:
        print("Wikipedia request timed out", flush=True)
        await message.answer("Wikipedia не ответила вовремя. Попробуй позже.")
        return

    except aiohttp.ClientError as exc:
        print(
            f"Wikipedia network error: {type(exc).__name__}",
            flush=True,
        )
        await message.answer("Не удалось соединиться с Wikipedia. Попробуй позже.")
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

    timeout = aiohttp.ClientTimeout(total=20)

    async with aiohttp.ClientSession(headers=HEADERS, timeout=timeout) as session:
        await dispatcher.start_polling(bot, session=session)


if __name__ == "__main__":
    asyncio.run(main())
