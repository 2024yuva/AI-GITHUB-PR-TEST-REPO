import pytest
from pydantic import ValidationError

from src.validator import ReviewResponse, validate_review


DIFF = """--- a/src/maths.py
+++ b/src/maths.py
@@ -1,2 +1,3 @@
 def average(numbers):
-    return 0
+    return sum(numbers) / len(numbers)
+
"""


def test_rejects_invalid_severity() -> None:
    with pytest.raises(ValidationError):
        ReviewResponse.model_validate(
            {
                "summary": "Issue found",
                "complexity": "low",
                "issues": [{"severity": "urgent", "file_path": "src/maths.py", "line_number": 2, "explanation": "Bad severity", "suggested_fix": "Use a valid severity", "evidence": "return sum(numbers) / len(numbers)"}],
            }
        )


def test_rejects_unchanged_line_reference() -> None:
    review = ReviewResponse.model_validate(
        {"summary": "Division by zero is possible.", "complexity": "low", "issues": [{"severity": "high", "file_path": "src/maths.py", "line_number": 1, "explanation": "An empty list makes len(numbers) zero.", "suggested_fix": "Guard an empty list before division.", "evidence": "return sum(numbers) / len(numbers)"}]}
    )
    with pytest.raises(ValueError, match="not an added diff line"):
        validate_review(review, DIFF)
