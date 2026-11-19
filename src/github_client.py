"""Small, dependency-free client for GitHub pull-request data."""

from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class GitHubAPIError(RuntimeError):
    """Raised when GitHub cannot provide the requested PR data."""


class DiffLimitError(GitHubAPIError):
    """Raised when a PR diff exceeds the configured review budget."""


class GitHubClient:
    def __init__(
        self,
        repository: str,
        token: str | None = None,
        max_diff_chars: int = 80_000,
    ) -> None:
        if repository.count("/") != 1:
            raise ValueError("repository must use owner/name format")
        if max_diff_chars < 1:
            raise ValueError("max_diff_chars must be positive")
        self.repository = repository
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.max_diff_chars = max_diff_chars

    def _request(self, path: str) -> object:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "pr-guardian",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = Request(f"https://api.github.com{path}", headers=headers)
        try:
            with urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code == 404:
                raise GitHubAPIError(f"Pull request or repository not found: {path}") from exc
            raise GitHubAPIError(f"GitHub API returned {exc.code} for {path}") from exc
        except URLError as exc:
            raise GitHubAPIError("GitHub API request failed") from exc

    def get_pull_request(self, number: int) -> dict[str, object]:
        data = self._request(f"/repos/{quote(self.repository, safe='/')}/pulls/{number}")
        if not isinstance(data, dict):
            raise GitHubAPIError("Unexpected pull-request response")
        return data

    def get_changed_files(self, number: int) -> list[dict[str, object]]:
        """Fetch all file pages, stopping before an oversized model payload."""
        files: list[dict[str, object]] = []
        total_chars = 0
        page = 1
        owner_repo = quote(self.repository, safe="/")
        while True:
            data = self._request(
                f"/repos/{owner_repo}/pulls/{number}/files?per_page=100&page={page}"
            )
            if not isinstance(data, list):
                raise GitHubAPIError("Unexpected changed-files response")
            for item in data:
                if not isinstance(item, dict):
                    raise GitHubAPIError("Unexpected changed-file entry")
                patch = item.get("patch")
                if isinstance(patch, str):
                    total_chars += len(patch)
                    if total_chars > self.max_diff_chars:
                        raise DiffLimitError(
                            f"PR diff exceeds configured {self.max_diff_chars}-character limit"
                        )
                files.append(item)
            if len(data) < 100:
                return files
            page += 1


def combine_patches(files: list[dict[str, object]]) -> str:
    """Create a model-ready unified diff with explicit paths for every patch."""
    chunks: list[str] = []
    for item in files:
        filename, patch = item.get("filename"), item.get("patch")
        if isinstance(filename, str) and isinstance(patch, str) and item.get("status") != "removed":
            chunks.append(f"--- a/{filename}\n+++ b/{filename}\n{patch}")
    return "\n\n".join(chunks)
