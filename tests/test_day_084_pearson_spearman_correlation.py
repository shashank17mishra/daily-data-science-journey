"""
Tests for Day 084: Pearson & Spearman Correlation Analysis Engine
"""

import pytest
import scipy.stats as stats
from learning.statistics.day_084_pearson_spearman_correlation import (
    compute_ranks,
    calculate_pearson,
    calculate_spearman,
    BivariateCorrelationAnalyzer
)


def test_compute_ranks_with_ties():
    data = [10.0, 20.0, 20.0, 30.0]
    expected = [1.0, 2.5, 2.5, 4.0]
    ranks = compute_ranks(data)
    assert ranks == pytest.approx(expected)


def test_pearson_perfect_linear():
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [2.0, 4.0, 6.0, 8.0, 10.0]
    res = calculate_pearson(x, y)

    assert pytest.approx(res.statistic, abs=1e-6) == 1.0
    assert pytest.approx(res.p_value, abs=1e-6) == 0.0
    assert res.ci_lower == pytest.approx(1.0)
    assert res.ci_upper == pytest.approx(1.0)


def test_pearson_matches_scipy():
    x = [1.2, 2.4, 3.1, 4.8, 5.5, 7.1]
    y = [3.1, 4.9, 2.8, 6.2, 8.0, 9.3]

    res = calculate_pearson(x, y)
    expected_r, expected_p = stats.pearsonr(x, y)

    assert res.statistic == pytest.approx(expected_r, abs=1e-5)
    assert res.p_value == pytest.approx(expected_p, abs=1e-5)


def test_spearman_perfect_monotonic_non_linear():
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [10.0, 100.0, 1000.0, 10000.0, 100000.0]

    pearson_res = calculate_pearson(x, y)
    spearman_res = calculate_spearman(x, y)

    assert spearman_res.statistic == pytest.approx(1.0)
    assert pearson_res.statistic < 0.90


def test_spearman_matches_scipy():
    x = [1.2, 2.4, 3.1, 4.8, 5.5, 7.1]
    y = [3.1, 4.9, 2.8, 6.2, 8.0, 9.3]

    res = calculate_spearman(x, y)
    expected_rho, expected_p = stats.spearmanr(x, y)

    assert res.statistic == pytest.approx(expected_rho, abs=1e-5)
    assert res.p_value == pytest.approx(expected_p, abs=1e-5)


def test_analyzer_detects_non_linear_trend():
    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    y = [1.0, 4.0, 9.0, 25.0, 100.0, 500.0, 2500.0]

    analyzer = BivariateCorrelationAnalyzer(x, y)
    result = analyzer.analyze()

    assert result["non_linear_monotonic_trend"] is True
    assert result["abs_difference"] > 0.1


def test_edge_cases_and_exceptions():
    with pytest.raises(ValueError, match="equal length"):
        calculate_pearson([1.0, 2.0], [1.0])

    with pytest.raises(ValueError, match="at least 3"):
        calculate_pearson([1.0, 2.0], [3.0, 4.0])

    with pytest.raises(ValueError, match="constant arrays"):
        calculate_pearson([2.0, 2.0, 2.0], [1.0, 2.0, 3.0])
