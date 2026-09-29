import asyncio

import aiohttp

from search_bot.github import HEADERS, search_github


async def main() -> None:

    timeout = aiohttp.ClientTimeout(total=20)

    async with aiohttp.ClientSession(
        headers=HEADERS,
        timeout=timeout,
    ) as session:
        results = await search_github(session, "python asyncio semaphore")

        if not results:
            print("GitHub не нашёл подходящих репозиториев")

        for result in results:
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
