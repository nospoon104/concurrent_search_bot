from html import unescape

import aiohttp

from search_bot.models import SearchResult


API_URL = "https://api.stackexchange.com/2.3/search/advanced"


def convert_stackoverflow_result(item: dict) -> SearchResult:
    accepted = "Да" if "accepted_answer_id" in item else "Нет"

    return SearchResult(
        title=unescape(item["title"]),
        description="Вопрос на Stack Overflow",
        url=item["link"],
        source="Stack Overflow",
        details=(
            f"Ответов: {item['answer_count']} · "
            f"Рейтинг: {item['score']} · "
            f"Принят ответ: {accepted}"
        ),
    )


async def search_stackoverflow(
    session: aiohttp.ClientSession,
    query: str,
) -> list[SearchResult]:
    params = {
        "site": "stackoverflow",
        "q": query,
        "pagesize": 2,
    }

    async with session.get(API_URL, params=params) as response:
        response.raise_for_status()
        data = await response.json()

    items = data["items"]

    return [convert_stackoverflow_result(item) for item in items]
