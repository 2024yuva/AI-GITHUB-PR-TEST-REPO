"""Human-readable, safe rendering of review results."""

from .schemas import ReviewResult


def github_comment(result: ReviewResult) -> str:
    lines = ["## PR Guardian", "", result.summary]
    if not result.findings:
        lines.extend(["", "No evidence-backed issues found in the reviewed changes."])
    for finding in result.findings:
        lines.extend(
            [
                "",
                f"### `{finding.severity.value}` - {finding.title}",
                f"[{finding.file}#L{finding.line_start}]({finding.file}#L{finding.line_start})",
                finding.explanation,
                f"> Evidence: {finding.evidence}",
            ]
        )
    lines.extend(
        [
            "",
            f"<sub>PR Guardian - {result.metadata.model} - {result.metadata.latency_ms} ms</sub>",
        ]
    )
    return "\n".join(lines)
