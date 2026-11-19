"""Compatibility import for the PR review service."""

from src.review.service import ReviewError, review_diff

__all__ = ["ReviewError", "review_diff"]
