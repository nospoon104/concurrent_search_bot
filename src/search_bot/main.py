import asyncio
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет! Отправь текстовый запрос — пока я просто повторю его."
    )


@router.message()
async def handle_message(message: Message) -> None:
    if message.text is None:
        await message.answer("Пока только текстовые сообщения")
        return

    query = message.text.strip()

    if not query:
        await message.answer("Нужен непустой поисковой запрос.")
        return

    await message.answer(f"Получен запрос: {query}")


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
