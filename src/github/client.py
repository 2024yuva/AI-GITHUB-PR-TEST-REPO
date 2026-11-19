"""GitHub REST API client."""

from __future__ import annotations

import json
import os
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


class GitHubAPIError(RuntimeError):
    """Raised when the GitHub REST API cannot complete a request."""


class GitHubClient:
    def __init__(self, repository: str, token: str | None = None) -> None:
        if "/" not in repository:
            raise ValueError("repository must use the owner/name format")
        self.repository = repository
        self.token = token or os.getenv("GITHUB_TOKEN")

    def _request(self, path: str, method: str = "GET", payload: object | None = None) -> object:
        url = f"https://api.github.com{path}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "pr-guardian",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        if data:
            headers["Content-Type"] = "application/json"
        request = Request(url, headers=headers, data=data, method=method)
        try:
            with urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise GitHubAPIError(
                f"GitHub API returned {exc.code} for {path}"
            ) from exc
        except Exception as exc:
            raise GitHubAPIError(f"GitHub API request failed for {path}") from exc

    def _get(self, path: str) -> object:
        return self._request(path)

    def get_pull_request(self, number: int) -> dict:
        owner_repo = quote(self.repository, safe="/")
        data = self._get(f"/repos/{owner_repo}/pulls/{number}")
        if not isinstance(data, dict):
            raise GitHubAPIError("Unexpected pull-request response")
        return data

    def get_changed_files(self, number: int) -> list[dict]:
        owner_repo = quote(self.repository, safe="/")
        data = self._get(f"/repos/{owner_repo}/pulls/{number}/files?per_page=100")
        if not isinstance(data, list):
            raise GitHubAPIError("Unexpected changed-files response")
        return data

    def create_issue_comment(self, number: int, body: str) -> dict:
        """Create a regular PR conversation comment."""
        owner_repo = quote(self.repository, safe="/")
        data = self._request(
            f"/repos/{owner_repo}/issues/{number}/comments",
            method="POST",
            payload={"body": body},
        )
        if not isinstance(data, dict):
            raise GitHubAPIError("Unexpected comment response")
        return data
