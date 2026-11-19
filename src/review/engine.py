"""Review engine entry point."""

from __future__ import annotations

import json
import os
from time import monotonic

from anthropic import Anthropic
from pydantic import ValidationError

from .prompts import BASELINE_SYSTEM_PROMPT, build_baseline_prompt
from .schemas import ReviewMetadata, ReviewResult, ReviewStatus
from .validator import validate_evidence


DEFAULT_MODEL = "claude-sonnet-4-20250514"
MAX_DIFF_CHARS = 80_000


def review_diff(
    diff_text: str,
    mode: str = "baseline",
    model: str | None = None,
    allowed_files: set[str] | None = None,
) -> ReviewResult:
    """Run one bounded Anthropic review and return only validated findings."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is required for analysis")
    if not diff_text.strip():
        raise RuntimeError("No reviewable diff was supplied")
    if len(diff_text) > MAX_DIFF_CHARS:
        raise RuntimeError(f"Diff exceeds the {MAX_DIFF_CHARS:,}-character review limit")

    started = monotonic()
    selected_model = model or os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL)
    response = Anthropic(api_key=api_key).messages.create(
        model=selected_model,
        max_tokens=1800,
        temperature=0,
        system=BASELINE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_baseline_prompt(diff_text)}],
    )
    raw = "".join(block.text for block in response.content if block.type == "text")
    try:
        payload = json.loads(raw)
        payload.pop("metadata", None)
        result = ReviewResult.model_validate(
            {
                **payload,
                "metadata": _metadata(response, mode, selected_model, started),
            }
        )
    except (json.JSONDecodeError, ValidationError) as exc:
        raise RuntimeError("Provider returned an invalid review JSON response") from exc

    allowed_files = allowed_files or _changed_files(diff_text)
    findings = validate_evidence(result.findings, allowed_files, diff_text)
    status = ReviewStatus.REVIEWED if findings else ReviewStatus.NO_FINDINGS
    return result.model_copy(update={"status": status, "findings": findings})


def _metadata(response: object, mode: str, model: str, started: float) -> ReviewMetadata:
    usage = getattr(response, "usage")
    return ReviewMetadata(
        mode=mode,
        provider="anthropic",
        model=model,
        latency_ms=round((monotonic() - started) * 1000),
        input_tokens=getattr(usage, "input_tokens", 0),
        output_tokens=getattr(usage, "output_tokens", 0),
        estimated_cost_usd=0.0,
    )


def _changed_files(diff_text: str) -> set[str]:
    return {
        line[6:] for line in diff_text.splitlines() if line.startswith("+++ b/")
    }
