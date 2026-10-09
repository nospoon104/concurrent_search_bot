from collections.abc import Awaitable, Callable
from time import perf_counter

import aiohttp
import asyncio
import logging

from search_bot.models import ProviderOutcome, SearchResult

type SearchFunction = Callable[
    [aiohttp.ClientSession, str],
    Awaitable[list[SearchResult]],
]

logger = logging.getLogger(__name__)


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
        self._providers = tuple(providers)
        self._provider_timeout = provider_timeout
        self._semaphore = asyncio.Semaphore(max_concurrent_providers)
        self._search_timeout = search_timeout

    async def search(self, query: str) -> list[ProviderOutcome]:
        if not self._providers:
            return []

        tasks = [
            asyncio.create_task(self._search_one(source, search_function, query))
            for source, search_function in self._providers
        ]

        try:
            done, pending = await asyncio.wait(
                tasks,
                timeout=self._search_timeout,
            )

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

        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()

            await asyncio.gather(*tasks, return_exceptions=True)

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
            logger.warning(
                "%s: API вернул HTTP %s",
                source,
                exc.status,
                exc_info=True,
            )

            outcome = ProviderOutcome(
                source=source,
                error=(
                    "Не удалось получить результаты из этого источника. "
                    "Попробуй повторить запрос позже."
                ),
            )

        except TimeoutError:
            logger.warning(
                "%s: превышено время ожидания провайдера",
                source,
            )

            outcome = ProviderOutcome(
                source=source,
                error="Источник не ответил вовремя. Попробуй позже.",
            )

        except aiohttp.ClientError:
            logger.warning(
                "%s: сетевая ошибка при обращении к API",
                source,
                exc_info=True,
            )

            outcome = ProviderOutcome(
                source=source,
                error="Не удалось связаться с источником. Попробуй позже.",
            )

        elapsed = perf_counter() - started

        logger.info(
            "%s: ожидание и выполнение заняли %.2f с",
            source,
            elapsed,
        )

        return outcome
