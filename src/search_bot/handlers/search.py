from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from search_bot.config import Settings
from search_bot.formatting import format_search_outcomes
from search_bot.search_service import SearchService


router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет! Напиши запрос — поищу в Wikipedia, GitHub " "и Stack Overflow."
    )


@router.message()
async def handle_message(
    message: Message,
    search_service: SearchService,
    settings: Settings,
) -> None:
    if message.text is None:
        await message.answer("Пока только текстовые сообщения.")
        return

    query = message.text.strip()

    if not query:
        await message.answer("Нужен непустой поисковый запрос.")
        return

    if len(query) > settings.max_query_length:
        await message.answer(
            "Запрос слишком длинный. "
            f"Используй не больше {settings.max_query_length} символов."
        )
        return

    outcomes = await search_service.search(query)
    messages = format_search_outcomes(outcomes)

    for text in messages:
        await message.answer(
            text,
            parse_mode=ParseMode.HTML,
        )
