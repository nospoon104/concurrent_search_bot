import aiohttp
from aiogram import Dispatcher

from search_bot.config import Settings
from search_bot.github import search_github
from search_bot.handlers.search import router
from search_bot.search_service import SearchService
from search_bot.stackoverflow import search_stackoverflow
from search_bot.wikipedia import search_wikipedia


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    return dispatcher


def create_search_service(
    session: aiohttp.ClientSession,
    settings: Settings,
) -> SearchService:
    service = SearchService(
        session=session,
        provider_timeout=settings.provider_timeout,
        max_concurrent_providers=settings.max_concurrent_providers,
        search_timeout=settings.search_timeout,
    )

    service.register_provider("Wikipedia", search_wikipedia)
    service.register_provider("GitHub", search_github)
    service.register_provider(
        "Stack Overflow",
        search_stackoverflow,
    )

    return service
