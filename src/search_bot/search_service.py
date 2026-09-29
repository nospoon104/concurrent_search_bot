from collections.abc import Awaitable, Callable
from time import perf_counter

import aiohttp

from search_bot.models import ProviderOutcome, SearchResult

type SearchFunction = Callable[
    [aiohttp.ClientSession, str],
    Awaitable[list[SearchResult]],
]


class SearchService:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        providers: list[tuple[str, SearchFunction]],
    ) -> None:
        self._session = session
        self._providers = providers

    async def search(self, query: str) -> list[ProviderOutcome]:
        outcomes = []

        for source, search_function in self._providers:
            outcome = await self._search_one(
                source,
                search_function,
                query,
            )
            outcomes.append(outcome)

        return outcomes

    async def _search_one(
        self,
        source: str,
        search_function: SearchFunction,
        query: str,
    ) -> ProviderOutcome:

        started = perf_counter()

        try:
            results = await search_function(self._session, query)
            outcome = ProviderOutcome(
                source=source,
                results=results,
            )

        except aiohttp.ClientResponseError as exc:
            outcome = ProviderOutcome(
                source=source,
                error=f"Ошибка HTTP {exc.status}.",
            )

        except TimeoutError:
            outcome = ProviderOutcome(
                source=source,
                error="Источник не ответил вовремя.",
            )

        except aiohttp.ClientError as exc:
            print(
                f"{source}: сетевая ошибка {type(exc).__name__}",
                flush=True,
            )
            outcome = ProviderOutcome(
                source=source,
                error="Не удалось соединиться с источником.",
            )

        elapsed = perf_counter() - started
        print(
            f"{source}: обращение заняло {elapsed:.2f} с",
            flush=True,
        )

        return outcome
