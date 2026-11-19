# PR Guardian: Functional and Non-Functional Requirements

## Functional requirements

### FR-1: Pull-request ingestion

- The system must accept a GitHub pull-request repository, pull-request number,
  base commit, and head commit.
- It must retrieve PR metadata and changed files through the GitHub REST API.
- It must support the `pull_request` events `opened` and `synchronize`.
- It must identify added, modified, deleted, and renamed files.

### FR-2: Diff parsing

- The system must parse unified diffs into changed hunks and changed line ranges.
- It must preserve file paths and new-file line locations.
- It must handle deleted files and binary or unsupported files safely.
- It must limit review input to a configurable maximum diff size.

### FR-3: Repository context retrieval

- The system must retrieve source context relevant to changed symbols and imports.
- The MVP must support direct file lookup and Python AST-based symbol discovery.
- Cross-file references must be available to the review engine when repository
  access is possible.
- Context retrieval must record source paths and line ranges used as evidence.

### FR-4: Review analysis

- The system must analyze code for bugs, logic errors, edge cases, security issues,
  and reliability problems.
- It must distinguish changed code, supporting repository context, and static
  analysis observations.
- It must not report a finding unless the finding has a source location and evidence.
- It must support separate baseline and improved review modes for evaluation.

### FR-5: Finding validation

- The system must validate finding structure with Pydantic.
- It must reject evidence that does not refer to a changed file or relevant source
  location.
- It must reject duplicate findings for the same issue and location.
- It must not substitute an unsupported LLM explanation for missing source evidence.
- Static and LLM findings must use the same normalized output schema.

### FR-6: Review output

- The system must produce a structured review containing a summary, findings,
  complexity rating, review metadata, and result status.
- Each finding must contain a title, category, severity, affected file, line range,
  explanation, evidence, and confidence.
- The system must format findings for GitHub Actions logs and optional Slack posting.
- The MVP must not approve or merge pull requests.

### FR-7: Metrics and benchmark support

- The system must compare findings against ground-truth file and line annotations.
- It must calculate precision, recall, F1, and false-positive rate.
- It must measure review latency, model input/output usage, and estimated cost.
- It must write benchmark results in a machine-readable format.

### FR-8: Safe failure behavior

- Authentication, API, parsing, and model failures must produce a clear result
  rather than silent success.
- The workflow must preserve an actionable failure log.
- Unavailable repository context must be recorded and must not be represented as
  successful context retrieval.

## Non-functional requirements

### NFR-1: Evidence quality

- Every reported finding must be traceable to a source location.
- Findings without verifiable evidence must be excluded from the final review.
- Cross-file claims must identify the supporting file and symbol or call path.

### NFR-2: Reliability

- Transient GitHub API and model requests should use bounded retries.
- Timeouts must prevent a review job from running indefinitely.
- Review failures must be attributable to a named ingestion, parsing, analysis,
  validation, or delivery stage.

### NFR-3: Performance

- The MVP must report end-to-end latency in benchmark results.
- Diff and context limits must be configurable.
- The review engine must avoid sending more repository content than required for
  the changed code.

### NFR-4: Cost awareness

- Each benchmark run must record provider, model, input/output token counts,
  elapsed time, and estimated cost.
- The workflow must support limits on diff size, context size, and review attempts.

### NFR-5: Security

- API keys and webhook secrets must be supplied through GitHub Actions secrets.
- Secrets must not appear in logs, review findings, benchmark artifacts, or source
  files.
- Repository content must be sent to the configured model provider only with the
  corresponding repository's authorization and as required for review execution.

### NFR-6: Reproducibility

- A benchmark fixture must include repository, base/head revision, ground truth,
  and expected affected lines.
- Review configuration and model identity must be recorded with each result.
- Prompt and schema changes must be testable through fixture-based tests.

### NFR-7: Maintainability

- GitHub access, diff parsing, review prompts, schemas, validation, static analysis,
  notifications, and metrics must have separate modules.
- Python code must pass the repository's pytest and Ruff checks.
- Public interfaces must use explicit types and validated inputs.

### NFR-8: Privacy

- The system must document when repository content is transmitted externally.
- Benchmark fixtures must avoid credentials and unnecessary private data.
- Logs and artifacts must retain only the minimum repository evidence needed for
  diagnosis and evaluation.

## Acceptance criteria for the requirements phase

- A pull request on or synchronize event produces a structured review attempt.
- A finding cannot reach output without a valid source location and evidence.
- Clean and buggy fixtures can be evaluated with the documented metric functions.
- Latency and cost are emitted for every benchmark run.
- Missing credentials, API failures, invalid model output, and oversized diffs
  fail visibly and do not produce success-shaped output.
