from html import escape

from search_bot.models import ProviderOutcome


TELEGRAM_MESSAGE_LIMIT = 4000

MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 300
MAX_DETAILS_LENGTH = 200
MAX_URL_LENGTH = 500


def _format_result(result) -> str:
    lines = [
        escape(result.title[:MAX_TITLE_LENGTH]),
    ]

    if result.description:
        lines.append(escape(result.description[:MAX_DESCRIPTION_LENGTH]))

    if result.details:
        lines.append(escape(result.details[:MAX_DETAILS_LENGTH]))

    lines.append(escape(result.url[:MAX_URL_LENGTH]))

    return "\n".join(lines)


def _split_units(units: list[str]) -> list[str]:
    messages: list[str] = []
    current_units: list[str] = []
    current_length = 0

    for unit in units:
        additional_length = len(unit)

        if current_units:
            additional_length += 2  # два символа "\n\n"

        if (
            current_units
            and current_length + additional_length > TELEGRAM_MESSAGE_LIMIT
        ):
            messages.append("\n\n".join(current_units))
            current_units = [unit]
            current_length = len(unit)
            continue

        current_units.append(unit)
        current_length += additional_length

    if current_units:
        messages.append("\n\n".join(current_units))

    return messages


def format_search_outcomes(
    outcomes: list[ProviderOutcome],
) -> list[str]:
    if not outcomes:
        return ["Поиск не вернул результатов."]

    units: list[str] = []

    for outcome in outcomes:
        heading = f"<b>{escape(outcome.source)}</b>"

        if outcome.error is not None:
            units.append(f"{heading}\n{escape(outcome.error)}")
            continue

        if not outcome.results:
            units.append(f"{heading}\nНичего не найдено.")
            continue

        for result in outcome.results:
            units.append(f"{heading}\n{_format_result(result)}")

    return _split_units(units)
