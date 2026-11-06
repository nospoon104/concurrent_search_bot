from html import escape


from search_bot.models import ProviderOutcome


def format_search_outcomes(
    outcomes: list[ProviderOutcome],
) -> str:
    sections = []

    for outcome in outcomes:
        lines = [f"<b>{escape(outcome.source)}</b>"]

        if outcome.error is not None:
            lines.append(escape(outcome.error))

        elif not outcome.results:
            lines.append("Ничего не найдено.")

        else:
            for result in outcome.results:
                lines.append("")
                lines.append(escape(result.title[:200]))

                if result.description:
                    lines.append(escape(result.description[:300]))

                if result.details:
                    lines.append(escape(result.details[:200]))

                lines.append(escape(result.url[:500]))

        sections.append("\n".join(lines))

    return "\n\n".join(sections)
