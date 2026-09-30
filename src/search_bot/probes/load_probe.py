import asyncio
from time import perf_counter
import aiohttp

from search_bot.models import SearchResult
from search_bot.search_service import SearchService


active = 0
peak_active = 0


async def fake_provider(
    session: aiohttp.ClientSession,
    query: str,
) -> list[SearchResult]:
    global active, peak_active

    active += 1
    peak_active = max(peak_active, active)

    try:
        await asyncio.sleep(0.5)
        return []
    finally:
        active -= 1


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        service = SearchService(
            session=session,
            providers=[
                ("Источник A", fake_provider),
                ("Источник B", fake_provider),
                ("Источник C", fake_provider),
            ],
            provider_timeout=0.7,
            max_concurrent_providers=1,
            search_timeout=1.0,
        )

        started = perf_counter()

        result = await asyncio.gather(*(service.search(f"query-{i}") for i in range(5)))
        print(result)
        print(f"Общее время: {perf_counter() - started:.2f} с")

    print(f"\nПиковое число активных провайдеров: {peak_active}")
    print(f"Активных после завершения: {active}")


if __name__ == "__main__":
    asyncio.run(main())
