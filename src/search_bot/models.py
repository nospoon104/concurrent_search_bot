from dataclasses import dataclass, field


@dataclass(frozen=True)
class SearchResult:
    title: str
    description: str
    url: str
    source: str
    details: str = ""


@dataclass(frozen=True)
class ProviderOutcome:
    source: str
    results: list[SearchResult] = field(default_factory=list)
    error: str | None = None
