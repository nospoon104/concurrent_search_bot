import asyncio
from html import unescape
import aiohttp

from search_bot.models import SearchResult

from search_bot.stackoverflow import search_stackoverflow

API_URL = "https://api.stackexchange.com/2.3/search/advanced"

PARAMS = {
    "site": "stackoverflow",
    "q": "python asyncio semaphore",
    "pagesize": 2,
}


async def main() -> None:
    timeout = aiohttp.ClientTimeout(total=20)

    async with aiohttp.ClientSession(
        headers={"User-Agent": "ConcurrentSearchBot/0.1 (educational project)"},
        timeout=timeout,
    ) as session:
        results = await search_stackoverflow(session, "python asyncio semaphore")

    if not results:
        print("Stack Overflow не нашёл вопросов.")
        return

    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
