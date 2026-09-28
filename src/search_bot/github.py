import aiohttp

from search_bot.models import SearchResult

API_URL = "https://api.github.com/search/repositories"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "ConcurrentSearchBot/0.1 (educational project)",
}


def convert_gh_result(item: dict) -> SearchResult:
    language = item["language"] or "Не указан"
    description = item["description"] or "Описание не указано"

    return SearchResult(
        title=item["full_name"],
        description=description,
        url=item["html_url"],
        source="GitHub",
        details=f"⭐ {item['stargazers_count']} · Язык: {language}",
    )


async def search_github(
    session: aiohttp.ClientSession,
    query: str,
) -> list[SearchResult]:
    params = {"q": query, "per_page": 2}

    async with session.get(API_URL, params=params) as response:
        response.raise_for_status()
        data = await response.json()

    items = data["items"]

    return [convert_gh_result(item) for item in items]
