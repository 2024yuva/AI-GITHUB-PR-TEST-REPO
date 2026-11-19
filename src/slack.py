"""Slack Incoming Webhook formatting and delivery."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.validator import ReviewResponse


class SlackDeliveryError(RuntimeError):
    """Raised when a Slack webhook cannot accept the review."""


def format_review(pr_title: str, review: ReviewResponse) -> str:
    lines = [f"*PR Guardian review:* {pr_title}", review.summary]
    if not review.issues:
        lines.append("No actionable, evidence-supported issues found.")
    for issue in review.issues:
        lines.extend(
            [
                f"*{issue.severity.value.upper()}* — `{issue.file_path}:{issue.line_number}`",
                issue.explanation,
                f"Suggested fix: {issue.suggested_fix}",
            ]
        )
    lines.append(f"Complexity: *{review.complexity.value}*")
    return "\n".join(lines)


def send_review(webhook_url: str, text: str) -> None:
    request = Request(
        webhook_url,
        data=json.dumps({"text": text}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=15) as response:
            if not 200 <= response.status < 300:
                raise SlackDeliveryError(f"Slack webhook returned {response.status}")
    except (HTTPError, URLError) as exc:
        raise SlackDeliveryError("Slack webhook delivery failed") from exc
