from dataclasses import dataclass


# MediaWiki return result
@dataclass(frozen=True)
class SearchResult:
    title: str
    description: str
    url: str
    source: str

    def __repr__(self):
        return f"SearchResult(title = {self.title}; description = {self.description}; url = {self.url} | source: {self.source!r})"
