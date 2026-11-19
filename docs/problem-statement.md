# PR Guardian: Problem Statement and Target Users

## Product problem

Pull-request review is one of the most important opportunities to catch defects,
but review quality is uneven and expensive to scale. Large language models can
identify plausible issues quickly, yet standalone diff review is vulnerable to:

- Hallucinated findings not supported by repository code.
- Repetition of issues that a static tool or earlier review already covered.
- Missing context about imported modules, interfaces, call paths, and invariants.
- Inability to distinguish a real defect from a stylistic preference.
- No repeatable measurement of review precision or false-positive rate.

PR Guardian should provide an evidence-first review process. A reported finding
must include a changed or relevant source location, a concise explanation, and
enough evidence for a maintainer to reproduce or verify the concern.

## Target users

### Open-source maintainers

Maintainers need fast, consistent triage without replacing their judgment.
They benefit from concise findings, stable line locations, and direct links to
supporting code.

**Primary need:** reduce review time while preserving trust.

### Development teams

Engineering teams need a reviewer that integrates with pull-request workflows,
does not flood channels with weak warnings, and can operate within repository
security boundaries.

**Primary need:** gain review coverage with predictable cost and latency.

### SWE/AI engineering learners

Students and practitioners need a project that combines GitHub integration,
prompted analysis, validation, repository retrieval, evaluation, and deployment.

**Primary need:** demonstrate a complete, measurable engineering workflow.

### Portfolio reviewers

Recruiters and technical reviewers need evidence that the implementation solves
a defined problem and improves against a measurable baseline.

**Primary need:** see clear trade-offs, results, and reproducibility.

## Scope of the MVP

The MVP is a GitHub Actions workflow that reviews pull requests in Python
repositories. It retrieves PR metadata and changed files, analyzes the diff,
optionally retrieves relevant repository context, validates findings, and posts a
structured review.

The MVP should support:

- Pull requests opened or synchronized.
- Structured issue types and severity.
- Source-line references and evidence text.
- Baseline and improved review modes.
- Precision, recall, F1, false-positive, latency, and cost measurements.
- A benchmark containing clean and buggy pull-request fixtures.

## Out of scope for the MVP

- Autonomous merging or approval.
- Natural-language conversation with repository maintainers.
- Organization-wide policy configuration.
- Full support for every programming language.
- Always-on hosted SaaS deployment.
- Autonomous code modification or repair.
- Embedding-based retrieval unless the benchmark proves it provides enough value.

## Core measure of success

Success is not merely whether the model produces comments. It is whether the
system improves verified findings per review while keeping false positives low.

The initial benchmark compares:

1. An RTC-style baseline that sends a structured diff prompt to Claude.
2. A repository-aware review engine that retrieves and validates relevant context.
3. Static checks and evidence validation as separate quality controls.
