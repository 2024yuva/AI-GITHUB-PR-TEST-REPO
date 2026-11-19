from src.review.formatters import github_comment
from src.review.schemas import Complexity, ReviewMetadata, ReviewResult, ReviewStatus


def test_comment_renders_empty_review() -> None:
    result = ReviewResult(status=ReviewStatus.NO_FINDINGS, summary="Looks safe.", complexity=Complexity.LOW, metadata=ReviewMetadata(mode="baseline", provider="anthropic", model="test", latency_ms=1, input_tokens=0, output_tokens=0, estimated_cost_usd=0))
    assert "No evidence-backed issues" in github_comment(result)
