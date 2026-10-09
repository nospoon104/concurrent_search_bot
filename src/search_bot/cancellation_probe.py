import asyncio

import aiohttp

from search_bot.models import SearchResult
from search_bot.search_service import SearchService


active = 0


async def fake_provider(
    session: aiohttp.ClientSession,
    query: str,
) -> list[SearchResult]:
    global active

    active += 1
    print("Провайдер начал работу")

    try:
        await asyncio.sleep(5)
        return []
    finally:
        active -= 1
        print("Провайдер выполнил finally")


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        service = SearchService(
            session=session,
            providers=[
                ("Источник A", fake_provider),
                ("Источник B", fake_provider),
                ("Источник C", fake_provider),
            ],
            provider_timeout=20.0,
            max_concurrent_providers=3,
            search_timeout=20.0,
        )

        search_task = asyncio.create_task(service.search("test cancellation"))

        await asyncio.sleep(0.1)

        print("Отменяем общий поиск")
        search_task.cancel()

        try:
            await search_task
        except asyncio.CancelledError:
            print("Общий поиск отменён")

        print(f"Активных провайдеров после отмены: {active}")


if __name__ == "__main__":
    asyncio.run(main())
