"""Unit tests for descriptive statistics calculations."""

import math
import pytest
from learning.statistics.day_076_descriptive_stats import (
    WelfordAccumulator,
    compute_mean,
    compute_percentile,
    compute_std_dev,
    compute_summary_stats,
    compute_variance,
)


@pytest.fixture
def sample_data():
    return [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]


def test_compute_mean(sample_data):
    assert compute_mean(sample_data) == 5.0
    assert compute_mean([10.0]) == 10.0
    with pytest.raises(ValueError, match="empty dataset"):
        compute_mean([])


def test_compute_variance_sample_vs_population(sample_data):
    # Sample variance (ddof=1): 32 / 7 = 4.57142857...
    assert compute_variance(sample_data, ddof=1) == pytest.approx(
        32.0 / 7.0
    )
    # Population variance (ddof=0): 32 / 8 = 4.0
    assert compute_variance(sample_data, ddof=0) == pytest.approx(4.0)


def test_compute_std_dev(sample_data):
    sample_std = compute_std_dev(sample_data, ddof=1)
    pop_std = compute_std_dev(sample_data, ddof=0)

    assert sample_std == pytest.approx(math.sqrt(32.0 / 7.0))
    assert pop_std == pytest.approx(2.0)


def test_variance_invalid_ddof():
    with pytest.raises(ValueError, match="must be greater than ddof"):
        compute_variance([5.0], ddof=1)


def test_percentiles(sample_data):
    # Min (0th percentile), Median (50th percentile), Max (100th percentile)
    assert compute_percentile(sample_data, 0.0) == 2.0
    assert compute_percentile(sample_data, 50.0) == 4.5
    assert compute_percentile(sample_data, 100.0) == 9.0

    with pytest.raises(ValueError, match="Percentile must be between"):
        compute_percentile(sample_data, -5.0)


def test_summary_stats(sample_data):
    res = compute_summary_stats(sample_data, ddof=1)
    assert res.count == 8
    assert res.mean == 5.0
    assert res.variance == pytest.approx(32.0 / 7.0)
    assert res.std_dev == pytest.approx(math.sqrt(32.0 / 7.0))
    assert res.sem == pytest.approx(math.sqrt(32.0 / 7.0) / math.sqrt(8))
    assert res.min_val == 2.0
    assert res.max_val == 9.0
    assert res.median == 4.5
    assert res.iqr == res.q3 - res.q1


def test_welford_accumulator(sample_data):
    acc = WelfordAccumulator()
    for val in sample_data:
        acc.update(val)

    assert acc.count == 8
    assert acc.mean == pytest.approx(5.0)
    assert acc.variance(ddof=1) == pytest.approx(32.0 / 7.0)
    assert acc.variance(ddof=0) == pytest.approx(4.0)
    assert acc.std_dev(ddof=1) == pytest.approx(math.sqrt(32.0 / 7.0))


def test_welford_merge(sample_data):
    part1 = sample_data[:4]
    part2 = sample_data[4:]

    acc1 = WelfordAccumulator()
    for v in part1:
        acc1.update(v)

    acc2 = WelfordAccumulator()
    for v in part2:
        acc2.update(v)

    merged = acc1.merge(acc2)
    assert merged.count == 8
    assert merged.mean == pytest.approx(5.0)
    assert merged.variance(ddof=1) == pytest.approx(32.0 / 7.0)
