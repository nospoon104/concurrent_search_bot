# import asyncio
# from time import perf_counter


# async def fake_search(source: str, delay: float) -> str:
#     print(f"{source}: начал")
#     await asyncio.sleep(delay)
#     print(f"{source}: закончил")
#     return source


# async def sequential() -> list[str]:
#     results = []

#     for source, delay in (
#         ("Wikipedia", 1.0),
#         ("GitHub", 1.5),
#         ("Stack Overflow", 0.5),
#     ):
#         result = await fake_search(source, delay)
#         results.append(result)

#     return results


# async def concurrent() -> list[str]:

#     results = asyncio.gather(
#         fake_search("Wikipedia", 1.0),
#         fake_search("GitHub", 1.5),
#         fake_search("Stack Overflow", 0.5),
#     )

#     return await results


# async def main() -> None:
#     started = perf_counter()
#     results = await concurrent()
#     elapsed = perf_counter() - started

#     print("Результаты:", results)
#     print(f"Прошло: {elapsed:.2f} с")


# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
from time import perf_counter

import aiohttp

from search_bot.models import SearchResult
from search_bot.search_service import SearchService


async def fake_wikipedia(
    session: aiohttp.ClientSession,
    query: str,
) -> list[SearchResult]:
    print("Wikipedia: начала")
    await asyncio.sleep(1.0)
    print("Wikipedia: закончила")

    return [
        SearchResult(
            title=f"Статья: {query}",
            description="Тестовый результат",
            url="https://example.org/wiki",
            source="Wikipedia",
        )
    ]


async def fake_github(
    session: aiohttp.ClientSession,
    query: str,
) -> list[SearchResult]:
    print("GitHub: начал")
    await asyncio.sleep(1.5)
    print("GitHub: начал долгую работу")
    await asyncio.sleep(5)
    print("GitHub: закончил долгую работу")
    return []


async def fake_stackoverflow(
    session: aiohttp.ClientSession,
    query: str,
) -> list[SearchResult]:
    print("Stack Overflow: начал")
    await asyncio.sleep(0.5)
    print("Stack Overflow: закончил")

    return []


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        service = SearchService(
            session=session,
            providers=[
                ("Wikipedia", fake_wikipedia),
                ("GitHub", fake_github),
                ("Stack Overflow", fake_stackoverflow),
            ],
            provider_timeout=3.0,
            max_concurrent_providers=3,
        )

        started = perf_counter()
        outcomes = await service.search("python")
        elapsed = perf_counter() - started

    print(f"\nОбщее время: {elapsed:.2f} с")

    for outcome in outcomes:
        print(
            f"{outcome.source}: "
            f"результатов={len(outcome.results)}, "
            f"ошибка={outcome.error!r}"
        )


if __name__ == "__main__":
    asyncio.run(main())
