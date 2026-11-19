# PR Guardian

PR Guardian reviews GitHub pull-request diffs with Claude and sends a concise,
evidence-backed result to Slack. It is a reviewer assistant: it does not execute
PR code, approve changes, or merge pull requests.

## Architecture

```text
GitHub pull_request event
  -> GitHub REST API (metadata + paginated file patches)
  -> Claude structured review
  -> Pydantic evidence and changed-line validation
  -> Slack Incoming Webhook
```

The workflow checks out the trusted base revision only, then asks GitHub's API
for the PR diff. It never runs code supplied by the pull request.

## Installation

Python 3.11+ is required.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Environment configuration

Copy `.env.example` to `.env` and supply values through your shell or a local
environment loader. Do not commit `.env`.

| Variable | Purpose |
| --- | --- |
| `ANTHROPIC_API_KEY` | Claude API credential |
| `ANTHROPIC_MODEL` | Optional model ID; defaults to Claude Sonnet |
| `GITHUB_TOKEN` | GitHub API token with pull-request read access |
| `GITHUB_REPOSITORY` | `owner/repository` |
| `PR_NUMBER` | Pull-request number |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL |
| `MAX_DIFF_CHARS` | Maximum aggregated patch size; default `80000` |

Run a local review without Slack delivery:

```powershell
python -m src.main --repository owner/repository --pr 123 --no-slack
```

## GitHub Actions setup

Add these repository secrets under **Settings → Secrets and variables → Actions**:

- `ANTHROPIC_API_KEY`
- `SLACK_WEBHOOK_URL`

Optionally add an `ANTHROPIC_MODEL` repository variable. The workflow runs only
for same-repository PRs opened by the repository owner, uses read-only GitHub
permissions, and does not expose secret values in logs.

## Example review output

```text
PR Guardian review: Guard averages
An empty list can fail.
HIGH — src/maths.py:2
Division by zero is possible.
Suggested fix: Return early for an empty list.
Complexity: low
```

## Known limitations

- Claude reviews only textual patches provided by GitHub; binary and oversized
  diffs are not analyzed.
- Findings must point at added lines and quote literal patch evidence, which can
  exclude valid issues requiring broad repository context.
- The MVP sends review content to Anthropic and Slack; use it only where that
  data flow is approved.
- A successful workflow means delivery succeeded, not that every review finding
  is correct. Always inspect the result.
