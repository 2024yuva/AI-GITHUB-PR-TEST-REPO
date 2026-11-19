# Model Provider and API Strategy

## Initial provider

PR Guardian uses Anthropic Claude as the initial model provider because the RTC
baseline and project plan already identify Claude as the first implementation.

The provider adapter must keep the model call separate from GitHub ingestion,
diff parsing, and output validation so that providers can be replaced later.

## MVP API strategy

- Use the GitHub REST API for PR metadata and changed files.
- Use Anthropic Messages API for review generation.
- Request structured JSON in the system and user prompts.
- Parse and validate provider output with Pydantic.
- Record model identity, token usage, latency, and estimated cost.
- Use bounded retries for transient provider and GitHub failures.

## Baseline and improved modes

The `baseline` mode sends only the changed diff and repository metadata.

The `improved` mode sends:

1. The changed diff.
2. Relevant directly retrieved repository source.
3. Python AST symbol context.
4. Ruff and Semgrep observations.

Both modes use the same review schema and metric definitions.

## Provider abstraction

Implementations should expose:

```python
def review(prompt: str) -> ProviderResponse:
    ...
```

The provider response must include raw text, input/output token counts, and
provider/model identity. Provider-specific response handling must not leak into
diff parsing or finding validation.

## Future provider policy

Additional providers may be added after the baseline is reproducible. Provider
selection must be explicit and comparable, not silently selected by fallback.
No fallback provider should run unless configuration permits it.
