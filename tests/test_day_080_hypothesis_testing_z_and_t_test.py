"""Tests for Day 080: Hypothesis Testing (Z-test & One-sample t-test)."""

import math
import pytest
import numpy as np
from scipy import stats

from learning.statistics.day_080_hypothesis_testing_z_and_t_test import (
    z_test,
    one_sample_t_test,
    HypothesisTestResult,
)


def test_z_test_two_sided_known_values():
    # Given a sample with mean 110, mu_0=100, pop_std=15, n=25
    # sem = 15 / 5 = 3. z = (110 - 100) / 3 = 10 / 3 = 3.333333...
    data = np.full(25, 110.0)
    res = z_test(data, pop_mean=100.0, pop_std=15.0, alpha=0.05, alternative="two-sided")

    expected_z = 10.0 / 3.0
    assert math.isclose(res.statistic, expected_z, rel_tol=1e-5)
    assert res.degrees_of_freedom is None
    assert res.reject_null is True
    assert res.p_value < 0.05
    assert res.confidence_interval[0] < 110.0 < res.confidence_interval[1]


def test_t_test_matches_scipy():
    np.random.seed(42)
    sample = np.random.normal(loc=10.5, scale=2.0, size=30)
    pop_mean = 10.0

    for alt in ["two-sided", "greater", "less"]:
        my_res = one_sample_t_test(sample, pop_mean=pop_mean, alpha=0.05, alternative=alt)
        scipy_res = stats.ttest_1samp(sample, popmean=pop_mean, alternative=alt)

        assert math.isclose(my_res.statistic, scipy_res.statistic, rel_tol=1e-5)
        assert math.isclose(my_res.p_value, scipy_res.pvalue, rel_tol=1e-5)
        assert my_res.degrees_of_freedom == len(sample) - 1


def test_directional_logic_greater_and_less():
    # High sample mean relative to mu0
    high_sample = np.array([15.0, 16.0, 14.0, 15.5, 14.5])
    mu0 = 10.0

    # Alternative 'greater': sample > mu0, so we EXPECT to reject null
    res_greater = one_sample_t_test(high_sample, pop_mean=mu0, alternative="greater")
    assert res_greater.reject_null is True
    assert res_greater.p_value < 0.05

    # Alternative 'less': sample > mu0, so we DO NOT reject null
    res_less = one_sample_t_test(high_sample, pop_mean=mu0, alternative="less")
    assert res_less.reject_null is False
    assert res_less.p_value > 0.5

    # Low sample mean relative to mu0
    low_sample = np.array([4.0, 5.0, 4.5, 5.5, 4.0])

    # Alternative 'less': sample < mu0, so we EXPECT to reject null
    res_low_less = one_sample_t_test(low_sample, pop_mean=mu0, alternative="less")
    assert res_low_less.reject_null is True
    assert res_low_less.p_value < 0.05

    # Alternative 'greater': sample < mu0, so we DO NOT reject null
    res_low_greater = one_sample_t_test(low_sample, pop_mean=mu0, alternative="greater")
    assert res_low_greater.reject_null is False
    assert res_low_greater.p_value > 0.5


def test_z_test_validation_errors():
    with pytest.raises(ValueError, match="Data array must not be empty"):
        z_test([], pop_mean=10.0, pop_std=2.0)

    with pytest.raises(ValueError, match="pop_std must be positive"):
        z_test([1, 2, 3], pop_mean=10.0, pop_std=0.0)

    with pytest.raises(ValueError, match="Alpha must be strictly between 0 and 1"):
        z_test([1, 2, 3], pop_mean=10.0, pop_std=2.0, alpha=1.5)

    with pytest.raises(ValueError, match="Alternative must be"):
        z_test([1, 2, 3], pop_mean=10.0, pop_std=2.0, alternative="invalid")


def test_t_test_validation_errors():
    with pytest.raises(ValueError, match="At least 2 observations"):
        one_sample_t_test([10.0], pop_mean=10.0)

    with pytest.raises(ValueError, match="Sample variance is zero"):
        one_sample_t_test([5.0, 5.0, 5.0], pop_mean=10.0)

    with pytest.raises(ValueError, match="Alpha must be strictly between 0 and 1"):
        one_sample_t_test([1.0, 2.0, 3.0], pop_mean=0.0, alpha=-0.1)
