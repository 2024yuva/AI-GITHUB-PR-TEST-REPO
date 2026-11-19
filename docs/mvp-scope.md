# PR Guardian: MVP Scope

## MVP objective

The MVP is a reproducible GitHub Actions code-review system for Python pull
requests. It must demonstrate evidence-first findings, repository-aware context,
baseline-versus-improved evaluation, and measurable review quality.

The MVP proves one central claim:

> Repository-aware, validated review findings reduce unsupported warnings while
> preserving useful bug detection.

## Included capabilities

### Pull-request integration

- GitHub Actions trigger for `pull_request` events `opened` and `synchronize`.
- Repository, PR number, base revision, head revision, and changed-file retrieval.
- Support for added, modified, deleted, and renamed files.
- Optional Slack delivery for human-readable review summaries.

### Diff analysis

- Unified-diff parsing into files, hunks, and changed line ranges.
- Configurable limits for diff size and review input size.
- Safe handling of unsupported, binary, and deleted files.

### Repository-aware review

- Direct retrieval of relevant source files.
- Python AST discovery of symbols, classes, functions, imports, and references.
- Cross-file context for directly relevant calls and definitions.
- Evidence for every finding, with file and line information.

### Review engine

- Anthropic Claude as the initial model provider.
- A baseline mode that reviews the diff with a structured prompt.
- An improved mode that combines diff, repository context, and static observations.
- Structured Pydantic output for summaries and findings.
- Finding validation for location, evidence, severity, category, and duplicates.

### Static analysis

- Ruff for configured Python lint and safety checks.
- Semgrep for security-focused rules.
- Static observations normalized into the same finding model as LLM findings.

### Evaluation

- Curated clean and buggy PR fixtures.
- Logic, edge-case, security, and cross-file bug cases.
- Ground-truth findings and affected lines.
- Precision, recall, F1, false-positive rate, latency, and cost reporting.
- Machine-readable benchmark output and documented baseline comparison.

### Delivery and reproducibility

- GitHub Actions logs containing review status and findings.
- Optional Slack summary posting.
- Environment variable template and documentation.
- Automated pytest and Ruff checks.

## Explicitly out of scope

### Product behavior

- Approving, rejecting, merging, or blocking pull requests.
- Automatic code repair or commit creation.
- Conversational chat with maintainers.
- General-purpose organization policy enforcement.
- Real-time IDE integration.
- A hosted SaaS control plane or multi-tenant deployment.

### Language and code coverage

- First-class support for languages other than Python.
- Build-system-wide analysis of every framework or dependency ecosystem.
- Complete data-flow, taint, or symbolic analysis.
- Guaranteed detection of every bug class.

### Repository intelligence

- Embeddings or vector search unless benchmark evidence justifies them.
- Tree-sitter implementation in the MVP; it may be introduced in later phases.
- Whole-repository indexing for every workflow run.
- Historical PR analysis across an organization's repositories.

### Integrations

- Slack is optional rather than a required review channel.
- A dashboard is optional and not required for the MVP.
- Jira, Linear, Microsoft Teams, and other issue systems are excluded.
- Custom model routing and multi-LLM orchestration are not MVP requirements.

### Benchmarking

- Claims of statistical significance without sufficient repeated fixtures.
- Production-grade label quality for arbitrary repositories.
- A universal benchmark that represents every Python project or bug type.

## MVP acceptance criteria

The MVP is complete when all of the following are demonstrated:

- A real or test GitHub PR triggers the workflow on open or synchronize.
- Changed files and diffs are retrieved and parsed successfully.
- The review returns a valid structured result or a clearly named failure.
- Every emitted finding has a source location and supporting evidence.
- Unsupported or duplicate findings are removed before delivery.
- Cross-file evidence is exercised in at least one benchmark fixture.
- Clean fixtures do not receive a flooding volume of unsupported warnings.
- Baseline and improved modes produce comparable, machine-readable metrics.
- Precision, recall, F1, false-positive rate, latency, and cost are documented.
- GitHub Actions logs and tests provide a reproducible demonstration.

## Prioritized implementation sequence

1. GitHub REST ingestion and diff parsing.
2. Pydantic review schema and finding validation.
3. Anthropic review prompt and baseline reviewer.
4. Python AST and direct source context retrieval.
5. Ruff and Semgrep static analysis.
6. Benchmark fixtures and ground-truth evaluation.
7. GitHub Actions workflow and optional Slack delivery.
8. Baseline-versus-improved experiments and portfolio documentation.
