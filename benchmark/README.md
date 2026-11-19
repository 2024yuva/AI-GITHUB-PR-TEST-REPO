# PR Guardian Benchmark

Benchmarks compare baseline diff-only review against the repository-aware,
evidence-validated review engine.

## Fixture format

Each fixture should record:

- Repository and base/head revisions.
- PR number or synthetic fixture identifier.
- Changed files and ground-truth findings.
- Affected file and line ranges.
- Bug category and severity.
- Whether the fixture is clean or buggy.

## Metrics

Precision, recall, F1, false-positive rate, latency, and provider cost are
calculated for each run. Finding IDs are normalized from file, line range, and
expected defect key before matching.
