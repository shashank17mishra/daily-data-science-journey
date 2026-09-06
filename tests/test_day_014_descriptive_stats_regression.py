import pytest
from learning.statistics.day_014_descriptive_stats_regression import compute_mean_and_variance, fit_simple_linear_regression

def test_compute_mean_and_variance():
    data = [10.0, 20.0, 30.0, 40.0, 50.0]
    mean, var = compute_mean_and_variance(data)
    assert mean == 30.0
    assert var == 250.0

def test_fit_simple_linear_regression():
    # Perfect linear relationship y = 2x + 1
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [3.0, 5.0, 7.0, 9.0, 11.0]
    intercept, slope, r2 = fit_simple_linear_regression(x, y)
    assert intercept == 1.0
    assert slope == 2.0
    assert r2 == 1.0
