from collections.abc import Awaitable, Callable
from time import perf_counter

import aiohttp
import asyncio

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
        *,
        provider_timeout: float,
        max_concurrent_providers: int,
        search_timeout: float,
    ) -> None:
        if provider_timeout <= 0:
            raise ValueError("provider_timeout должен быть больше нуля")
        if max_concurrent_providers < 1:
            raise ValueError("max_concurrent_providers должен быть не меньше 1")
        if search_timeout <= 0:
            raise ValueError("search_timeout должен быть больше нуля")

        self._session = session
        self._providers = providers
        self._provider_timeout = provider_timeout
        self._semaphore = asyncio.Semaphore(max_concurrent_providers)
        self._search_timeout = search_timeout

    async def search(self, query: str) -> list[ProviderOutcome]:
        tasks = [
            asyncio.create_task(self._search_one(source, search_function, query))
            for source, search_function in self._providers
        ]

        done, pending = await asyncio.wait(
            tasks,
            timeout=self._search_timeout,
        )

        for task in pending:
            task.cancel()

        if pending:
            await asyncio.gather(*pending, return_exceptions=True)

        outcomes = []

        for (source, _), task in zip(self._providers, tasks):
            if task in done:
                outcomes.append(task.result())
            else:
                outcomes.append(
                    ProviderOutcome(
                        source=source,
                        error="Превышено общее время поиска.",
                    )
                )

        return outcomes

    async def _search_one(
        self,
        source: str,
        search_function: SearchFunction,
        query: str,
    ) -> ProviderOutcome:

        started = perf_counter()

        try:
            async with self._semaphore:
                async with asyncio.timeout(self._provider_timeout):
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
