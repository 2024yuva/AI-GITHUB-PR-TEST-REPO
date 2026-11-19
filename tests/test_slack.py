from src.slack import format_review
from src.validator import ReviewResponse


def test_formats_finding_for_slack() -> None:
    review = ReviewResponse.model_validate(
        {"summary": "An empty list can fail.", "complexity": "low", "issues": [{"severity": "high", "file_path": "src/maths.py", "line_number": 2, "explanation": "Division by zero is possible.", "suggested_fix": "Return early for an empty list.", "evidence": "return sum(numbers) / len(numbers)"}]}
    )
    message = format_review("Guard averages", review)
    assert "*HIGH*" in message
    assert "`src/maths.py:2`" in message
    assert "Complexity: *low*" in message
