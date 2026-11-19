"""Anthropic adapter for bounded, structured PR reviews."""

from __future__ import annotations

import json
import os

from anthropic import Anthropic, APIError
from pydantic import ValidationError

from src.validator import ReviewResponse, validate_review

DEFAULT_MODEL = "claude-sonnet-4-20250514"
SYSTEM_PROMPT = """You are PR Guardian, a careful pull-request reviewer.
Report at most three actionable bugs in the supplied diff. Only report a finding when
the changed code provides direct evidence. Do not report style concerns, hypothetical
problems, or pre-existing issues. Never say code was executed, tested, or reproduced.
Return only JSON with summary, complexity (low|medium|high), and issues. Every issue
must contain severity (critical|high|medium|low), file_path, line_number, explanation,
suggested_fix, and evidence. Evidence must be an exact short excerpt from the diff."""


class ReviewError(RuntimeError):
    """Raised when Claude fails to return a valid review."""


def _parse_review_payload(raw: str) -> dict[str, object]:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        cleaned = cleaned.rsplit("```", 1)[0].strip()
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start < 0 or end <= start:
            raise
        payload = json.loads(cleaned[start : end + 1])
    if not isinstance(payload, dict):
        raise TypeError("Claude response must be a JSON object")
    return payload


def review_diff(diff_text: str, model: str | None = None) -> ReviewResponse:
    if not diff_text.strip():
        raise ReviewError("No reviewable text diff was supplied")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ReviewError("ANTHROPIC_API_KEY is required")
    try:
        response = Anthropic(api_key=api_key).messages.create(
            model=model or os.getenv("ANTHROPIC_MODEL") or DEFAULT_MODEL,
            max_tokens=1600,
            temperature=0,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"Review this diff:\n\n{diff_text}"}],
        )
        raw = "".join(block.text for block in response.content if block.type == "text")
        result = ReviewResponse.model_validate(_parse_review_payload(raw))
        return validate_review(result, diff_text)
    except (APIError, json.JSONDecodeError, ValidationError, TypeError, ValueError) as exc:
        raise ReviewError("Claude returned an invalid or unsupported review response") from exc
