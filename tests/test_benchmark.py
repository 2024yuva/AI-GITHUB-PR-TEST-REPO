from benchmark.evaluate import calculate_metrics


def test_calculate_metrics() -> None:
    metrics = calculate_metrics(
        ground_truth_ids={"src/a.py:10:bug"},
        predicted_ids={"src/a.py:10:bug", "src/b.py:20:false_positive"},
        clean_item_count=4,
    )

    assert metrics.true_positives == 1
    assert metrics.false_positives == 1
    assert metrics.false_negatives == 0
    assert metrics.precision == 0.5
    assert metrics.recall == 1.0
    assert metrics.false_positive_rate == 0.25
