"""Coordinate GitHub ingestion, Claude review validation, and Slack delivery."""

from __future__ import annotations

import argparse
import os

from src.github_client import GitHubAPIError, GitHubClient, combine_patches
from src.review import ReviewError, review_diff
from src.slack import SlackDeliveryError, format_review, send_review


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review a GitHub pull request")
    parser.add_argument("--repository", default=os.getenv("GITHUB_REPOSITORY"))
    parser.add_argument("--pr", type=int, default=int(os.getenv("PR_NUMBER", "0")))
    parser.add_argument(
        "--max-diff-chars", type=int, default=int(os.getenv("MAX_DIFF_CHARS", "80000"))
    )
    parser.add_argument("--no-slack", action="store_true", help="Print without webhook delivery")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.repository or args.pr < 1:
        raise SystemExit("GITHUB_REPOSITORY and a valid PR_NUMBER are required")
    try:
        client = GitHubClient(args.repository, max_diff_chars=args.max_diff_chars)
        pull_request = client.get_pull_request(args.pr)
        diff_text = combine_patches(client.get_changed_files(args.pr))
        review = review_diff(diff_text)
        title = str(pull_request.get("title", f"PR #{args.pr}"))
        message = format_review(title, review)
        print(message)
        if not args.no_slack:
            webhook_url = os.getenv("SLACK_WEBHOOK_URL")
            if not webhook_url:
                raise SystemExit("SLACK_WEBHOOK_URL is required unless --no-slack is used")
            send_review(webhook_url, message)
    except (GitHubAPIError, ReviewError, SlackDeliveryError) as exc:
        raise SystemExit(f"PR Guardian failed: {exc}") from exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
