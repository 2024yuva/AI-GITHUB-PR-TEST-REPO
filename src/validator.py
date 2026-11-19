"""Pydantic contracts and evidence validation for Claude review output."""

from __future__ import annotations

import re
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Complexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Issue(BaseModel):
    severity: Severity
    file_path: str = Field(min_length=1)
    line_number: int = Field(gt=0)
    explanation: str = Field(min_length=1)
    suggested_fix: str = Field(min_length=1)
    evidence: str = Field(min_length=1)

    @field_validator("file_path")
    @classmethod
    def repository_relative_path(cls, value: str) -> str:
        if value.startswith(("/", "\\")) or "\\" in value or ".." in value.split("/"):
            raise ValueError("file_path must be a repository-relative POSIX path")
        return value


class ReviewResponse(BaseModel):
    summary: str = Field(min_length=1)
    issues: list[Issue] = Field(default_factory=list, max_length=3)
    complexity: Complexity


HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(?P<line>\d+)(?:,\d+)? @@")


def changed_lines_by_file(diff_text: str) -> dict[str, set[int]]:
    """Map every added source line in a unified diff to its repository path."""
    lines_by_file: dict[str, set[int]] = {}
    current_file: str | None = None
    current_line: int | None = None
    for raw_line in diff_text.splitlines():
        if raw_line.startswith("+++ b/"):
            current_file = raw_line[6:]
            lines_by_file.setdefault(current_file, set())
            current_line = None
            continue
        match = HUNK.match(raw_line)
        if match:
            current_line = int(match.group("line"))
            continue
        if current_file is None or current_line is None:
            continue
        if raw_line.startswith("+") and not raw_line.startswith("+++"):
            lines_by_file[current_file].add(current_line)
            current_line += 1
        elif raw_line.startswith(" "):
            current_line += 1
    return lines_by_file


def validate_review(response: ReviewResponse, diff_text: str) -> ReviewResponse:
    """Reject claims not anchored to a changed file, line, and literal evidence."""
    changed_lines = changed_lines_by_file(diff_text)
    for issue in response.issues:
        if issue.file_path not in changed_lines:
            raise ValueError(f"Issue file is not in the changed diff: {issue.file_path}")
        if issue.line_number not in changed_lines[issue.file_path]:
            raise ValueError(
                f"Issue line is not an added diff line: {issue.file_path}:{issue.line_number}"
            )
        if issue.evidence not in diff_text:
            raise ValueError("Issue evidence is not present in the supplied diff")
    return response
