"""Precision, recall, false-positive, and latency metrics."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class BenchmarkMetrics:
    true_positives: int
    false_positives: int
    false_negatives: int
    precision: float
    recall: float
    f1: float
    false_positive_rate: float


def calculate_metrics(
    ground_truth_ids: set[str],
    predicted_ids: set[str],
    clean_item_count: int,
) -> BenchmarkMetrics:
    true_positives = len(ground_truth_ids & predicted_ids)
    false_positives = len(predicted_ids - ground_truth_ids)
    false_negatives = len(ground_truth_ids - predicted_ids)

    precision = true_positives / (true_positives + false_positives) if predicted_ids else 0.0
    recall = true_positives / (true_positives + false_negatives) if ground_truth_ids else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    false_positive_rate = (
        false_positives / clean_item_count if clean_item_count > 0 else 0.0
    )

    return BenchmarkMetrics(
        true_positives=true_positives,
        false_positives=false_positives,
        false_negatives=false_negatives,
        precision=precision,
        recall=recall,
        f1=f1,
        false_positive_rate=false_positive_rate,
    )


def metrics_as_dict(metrics: BenchmarkMetrics) -> dict:
    return asdict(metrics)
