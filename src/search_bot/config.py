import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    bot_token: str = field(repr=False)
    http_timeout: float = 20.0
    provider_timeout: float = 20.0
    search_timeout: float = 30.0
    max_concurrent_providers: int = 3
    max_query_length: int = 300


def load_settings() -> Settings:
    load_dotenv()

    token = os.getenv("BOT_TOKEN", "").strip()

    if not token:
        raise RuntimeError(
            "BOT_TOKEN не задан. " "Укажи его в окружении или в локальном файле .env."
        )

    return Settings(bot_token=token)
