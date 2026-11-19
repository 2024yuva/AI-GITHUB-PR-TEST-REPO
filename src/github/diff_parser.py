"""Parsing helpers for GitHub unified diffs."""

from __future__ import annotations

import re
from dataclasses import dataclass

HUNK_HEADER = re.compile(r"^@@ -\d+(?:,\d+)? \+(?P<start>\d+)(?:,(?P<count>\d+))? @@")


@dataclass(frozen=True)
class DiffHunk:
    start: int
    end: int
    lines: tuple[str, ...]


@dataclass(frozen=True)
class ParsedDiff:
    filename: str
    status: str
    hunks: tuple[DiffHunk, ...]


def parse_diff(filename: str, status: str, patch: str | None) -> ParsedDiff:
    if not patch:
        return ParsedDiff(filename=filename, status=status, hunks=())

    hunks: list[DiffHunk] = []
    current_start: int | None = None
    current_count: int = 1
    current_lines: list[str] = []

    def close_hunk() -> None:
        nonlocal current_start, current_count, current_lines
        if current_start is not None:
            end = current_start + max(current_count - 1, 0)
            hunks.append(DiffHunk(current_start, end, tuple(current_lines)))
        current_start = None
        current_count = 1
        current_lines = []

    for raw_line in patch.splitlines():
        match = HUNK_HEADER.match(raw_line)
        if match:
            close_hunk()
            current_start = int(match.group("start"))
            current_count = int(match.group("count") or "1")
            continue
        if current_start is None:
            continue
        if raw_line.startswith(("+", "-", " ")):
            current_lines.append(raw_line)

    close_hunk()
    return ParsedDiff(filename=filename, status=status, hunks=tuple(hunks))
