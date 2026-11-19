"""Pydantic contracts for PR reviews."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator


class ReviewStatus(str, Enum):
    REVIEWED = "reviewed"
    NO_FINDINGS = "no_findings"
    FAILED = "failed"


class FindingCategory(str, Enum):
    BUG = "bug"
    SECURITY = "security"
    LOGIC = "logic"
    EDGE_CASE = "edge_case"
    RELIABILITY = "reliability"
    QUALITY = "quality"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Complexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class FindingSource(str, Enum):
    LLM = "llm"
    STATIC = "static"
    HYBRID = "hybrid"


class Finding(BaseModel):
    title: str = Field(min_length=1)
    category: FindingCategory
    severity: Severity
    file: str = Field(min_length=1)
    line_start: int = Field(gt=0)
    line_end: int = Field(gt=0)
    explanation: str = Field(min_length=1)
    evidence: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    source: FindingSource

    @field_validator("file")
    @classmethod
    def validate_repository_path(cls, value: str) -> str:
        if value.startswith("/") or "\\" in value:
            raise ValueError("file must be a repository-relative POSIX path")
        return value

    @model_validator(mode="after")
    def validate_line_range(self) -> "Finding":
        if self.line_end < self.line_start:
            raise ValueError("line_end must be greater than or equal to line_start")
        return self


class ReviewMetadata(BaseModel):
    mode: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    latency_ms: int = Field(ge=0)
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    estimated_cost_usd: float = Field(ge=0.0)


class ReviewResult(BaseModel):
    status: ReviewStatus
    summary: str = Field(min_length=1)
    complexity: Complexity
    findings: list[Finding] = Field(default_factory=list)
    metadata: ReviewMetadata
