from src.review.service import _parse_review_payload


def test_parse_review_payload_accepts_markdown_code_fence() -> None:
    assert _parse_review_payload('```json\n{"summary": "ok"}\n```') == {
        "summary": "ok"
    }


def test_parse_review_payload_accepts_surrounding_text() -> None:
    assert _parse_review_payload('Here is the review:\n{"summary": "ok"}') == {
        "summary": "ok"
    }
