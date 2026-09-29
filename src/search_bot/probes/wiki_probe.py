import asyncio

import aiohttp

from search_bot.wikipedia import HEADERS, search_wikipedia


async def main() -> None:
    timeout = aiohttp.ClientTimeout(total=20)

    async with aiohttp.ClientSession(
        headers=HEADERS,
        timeout=timeout,
    ) as session:

        query = "python"
        results = await search_wikipedia(session, query)

    if not results:
        print(f"Wikipedia не нашла результатов по запросу {query!r}")
        return

    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
