"""Evidence and duplicate validation for review findings."""

from __future__ import annotations

from .schemas import Finding


def deduplicate(findings: list[Finding]) -> list[Finding]:
    seen: set[tuple[str, int, int, str]] = set()
    result: list[Finding] = []
    for finding in findings:
        key = (
            finding.file,
            finding.line_start,
            finding.line_end,
            finding.title.lower(),
        )
        if key not in seen:
            seen.add(key)
            result.append(finding)
    return result


def validate_evidence(
    findings: list[Finding], allowed_files: set[str], evidence_text: str = ""
) -> list[Finding]:
    validated: list[Finding] = []
    for finding in findings:
        if finding.file not in allowed_files:
            continue
        if not finding.evidence.strip():
            continue
        if evidence_text and finding.evidence not in evidence_text:
            continue
        validated.append(finding)
    return deduplicate(validated)
