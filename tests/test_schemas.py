import pytest
from pydantic import ValidationError

from src.review.schemas import Finding


def test_finding_rejects_reversed_line_range() -> None:
    with pytest.raises(ValidationError):
        Finding(
            title="Invalid range",
            category="bug",
            severity="high",
            file="src/example.py",
            line_start=20,
            line_end=10,
            explanation="Bad range",
            evidence="Changed code",
            confidence=0.8,
            source="llm",
        )
