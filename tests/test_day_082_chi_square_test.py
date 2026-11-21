"""Unit tests for Chi-Square Test of Independence implementation."""

import pytest
import numpy as np
from scipy.stats import chi2_contingency
from learning.statistics.day_082_chi_square_test import ChiSquareTest


def test_invalid_input_dimensions():
    with pytest.raises(ValueError, match="2-dimensional"):
        ChiSquareTest(np.array([1, 2, 3]))


def test_negative_values():
    with pytest.raises(ValueError, match="non-negative"):
        ChiSquareTest(np.array([[-1, 5], [10, 20]]))


def test_small_table_dimensions():
    with pytest.raises(ValueError, match="at least 2x2"):
        ChiSquareTest(np.array([[10, 20, 30]]))


def test_zero_sum_table():
    with pytest.raises(ValueError, match="entirely zero"):
        ChiSquareTest(np.zeros((2, 2)))


def test_expected_frequencies():
    obs = np.array([[10, 20], [20, 40]])
    tester = ChiSquareTest(obs)
    exp = tester.compute_expected()
    expected_target = np.array([[10.0, 20.0], [20.0, 40.0]])
    assert np.allclose(exp, expected_target)


def test_chi2_contingency_2x2_matching_scipy():
    obs = np.array([[10, 20], [30, 40]])
    tester = ChiSquareTest(obs)
    result = tester.analyze(correction=True)

    scipy_chi2, scipy_p, scipy_dof, scipy_exp = chi2_contingency(obs, correction=True)

    assert np.isclose(result["chi2_stat"], scipy_chi2)
    assert np.isclose(result["p_value"], scipy_p)
    assert result["degrees_of_freedom"] == scipy_dof
    assert np.allclose(result["expected"], scipy_exp)


def test_chi2_contingency_3x3_no_correction():
    obs = np.array([[12, 15, 25], [20, 8, 14], [5, 18, 30]])
    tester = ChiSquareTest(obs)
    result = tester.analyze(correction=False)

    scipy_chi2, scipy_p, scipy_dof, scipy_exp = chi2_contingency(obs, correction=False)

    assert np.isclose(result["chi2_stat"], scipy_chi2)
    assert np.isclose(result["p_value"], scipy_p)
    assert result["degrees_of_freedom"] == scipy_dof
    assert np.allclose(result["expected"], scipy_exp)


def test_cramers_v_bounds():
    obs = np.array([[50, 10], [10, 50]])
    tester = ChiSquareTest(obs)
    result = tester.analyze()
    v = result["cramers_v"]
    assert 0.0 <= v <= 1.0


def test_assumptions_check():
    obs_small = np.array([[1, 2], [3, 4]])
    tester_small = ChiSquareTest(obs_small)
    assumptions = tester_small.check_assumptions()
    assert assumptions["valid"] is False
    assert assumptions["min_expected"] < 5.0

    obs_large = np.array([[50, 60], [70, 80]])
    tester_large = ChiSquareTest(obs_large)
    assumptions_large = tester_large.check_assumptions()
    assert assumptions_large["valid"] is True
