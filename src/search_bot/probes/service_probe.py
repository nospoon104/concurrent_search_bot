import asyncio

import aiohttp

from search_bot.github import search_github
from search_bot.models import ProviderOutcome
from search_bot.search_service import SearchService
from search_bot.stackoverflow import search_stackoverflow
from search_bot.wikipedia import search_wikipedia


async def main() -> None:
    timeout = aiohttp.ClientTimeout(total=20)

    async with aiohttp.ClientSession(
        headers={
            "User-Agent": "ConcurrentSearchBot/0.1 (educational project)",
        },
        timeout=timeout,
    ) as session:
        service = SearchService(
            session=session,
            providers=[
                ("Wikipedia", search_wikipedia),
                ("GitHub", search_github),
                ("Stack Overflow", search_stackoverflow),
            ],
        )

        outcomes = await service.search("python asyncio semaphore")

    for outcome in outcomes:
        print(f"\nИсточник: {outcome.source}")

        if outcome.error is not None:
            print(f"Ошибка: {outcome.error}")
            continue

        print(f"Результатов: {len(outcome.results)}")

        for result in outcome.results:
            print(f"- {result.title}")


if __name__ == "__main__":
    asyncio.run(main())
