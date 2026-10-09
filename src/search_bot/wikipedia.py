from html import unescape
from urllib.parse import quote

import aiohttp

from search_bot.models import SearchResult
from search_bot.config import WIKIPEDIA_API_URL


HEADERS = {
    "User-Agent": "ConcurrentSearchBot/0.1 (educational project) (russkiywolk@yandex.ru)",
}


def convert_wikipedia_result(result: dict) -> SearchResult:
    title = result["title"]
    snippet = result["snippet"]

    description = unescape(
        snippet.replace('<span class="searchmatch">', "").replace("</span>", "")
    )

    article_path = quote(title.replace(" ", "_"), safe="")
    url = f"https://en.wikipedia.org/wiki/{article_path}"

    return SearchResult(
        title=title, description=description, url=url, source="Wikipedia"
    )


async def search_wikipedia(
    session: aiohttp.ClientSession,
    query: str,
) -> list[SearchResult]:

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": 2,
        "format": "json",
    }

    async with session.get(WIKIPEDIA_API_URL, params=params) as response:

        response.raise_for_status()

        data = await response.json()

    raw_result = data["query"]["search"]

    return [convert_wikipedia_result(result) for result in raw_result]
