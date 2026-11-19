# Security and Privacy Requirements

## Secrets

- Store Anthropic API credentials and Slack webhook URLs in GitHub Actions secrets.
- Grant the workflow only the GitHub permissions it needs.
- Never print environment variables or secret-bearing HTTP responses.
- Never commit `.env` files or credentials.
- Treat benchmark fixtures as public if they are committed.

## Repository access

- Read repository content only for the pull request being reviewed.
- Validate PR repository ownership and identifiers before API calls.
- Use bounded timeouts and maximum diff/context sizes.
- Do not follow arbitrary URLs or execute untrusted repository code.
- Run lint and static analysis with repository-specific untrusted-code cautions.

## External model data

The workflow must document that changed code and retrieved context may be sent to
Anthropic. Private repositories require repository administrators to approve this
data-flow choice.

No source-code upload must occur outside the configured provider. Model providers
must not be silently selected as fallback destinations.

## Safe output

- Redact secret-looking strings from findings and logs where possible.
- Never include environment variable values or authentication headers.
- Keep benchmark artifacts free of credentials and personal data.
- Link evidence to repository source rather than copying unnecessary large files.

## Prompt and tool security

- Treat repository content and diff text as untrusted data.
- Separate instructions from retrieved content.
- Do not allow model output to execute shell commands or edit repository files.
- Reject output that changes review status or introduces file operations.

## Reliability and auditability

- Log stage, provider, model, status, latency, and cost without secret values.
- Include a configuration version or prompt version with benchmark results.
- Fail visibly when authentication or required repository access is unavailable.
