import numpy as np
import pytest
from scipy import stats
from learning.statistics.day_086_simple_linear_regression import SimpleLinearRegression, RegressionSummary


def test_perfect_linear_fit():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = 2.0 * x + 3.0

    model = SimpleLinearRegression()
    model.fit(x, y)

    assert pytest.approx(model.beta_1, abs=1e-10) == 2.0
    assert pytest.approx(model.beta_0, abs=1e-10) == 3.0
    
    summary = model.summary()
    assert pytest.approx(summary.r_squared, abs=1e-10) == 1.0
    assert summary.residual_std_error == pytest.approx(0.0, abs=1e-10)


def test_synthetic_data_recovery_and_intervals():
    np.random.seed(42)
    true_beta_0 = 5.0
    true_beta_1 = 1.5
    n = 100
    x = np.linspace(0, 10, n)
    noise = np.random.normal(0, 0.5, n)
    y = true_beta_0 + true_beta_1 * x + noise

    model = SimpleLinearRegression()
    model.fit(x, y)

    summary = model.summary()

    # Parameter estimates close to ground truth
    assert pytest.approx(model.beta_1, abs=0.1) == true_beta_1
    assert pytest.approx(model.beta_0, abs=0.2) == true_beta_0

    # Test confidence interval for parameters
    ci_b0, ci_b1 = model.confidence_interval(alpha=0.05)
    assert ci_b0[0] <= true_beta_0 <= ci_b0[1]
    assert ci_b1[0] <= true_beta_1 <= ci_b1[1]

    # Test prediction interval vs confidence interval width
    x_test = np.array([5.0, 12.0])
    intervals = model.predict_interval(x_test, alpha=0.05)

    ci_width = intervals["ci_upper"] - intervals["ci_lower"]
    pi_width = intervals["pi_upper"] - intervals["pi_lower"]

    # Prediction interval must strictly be wider than confidence interval of mean
    assert np.all(pi_width > ci_width)


def test_input_validation():
    model = SimpleLinearRegression()

    # Mismatched lengths
    with pytest.raises(ValueError, match="same length"):
        model.fit([1, 2, 3], [1, 2])

    # Insufficient samples
    with pytest.raises(ValueError, match="At least 3 data points"):
        model.fit([1, 2], [3, 4])

    # Zero variance in X
    with pytest.raises(ValueError, match="Variance of x is zero"):
        model.fit([5, 5, 5], [1, 2, 3])

    # Unfitted model calls
    with pytest.raises(RuntimeError):
        model.predict([1, 2])

    with pytest.raises(RuntimeError):
        model.summary()

    with pytest.raises(RuntimeError):
        model.confidence_interval()


def test_statistical_equivalence_with_scipy():
    np.random.seed(123)
    x = np.random.uniform(1, 20, size=30)
    y = 3.2 * x - 4.1 + np.random.normal(0, 2.0, size=30)

    model = SimpleLinearRegression()
    model.fit(x, y)
    summary = model.summary()

    scipy_res = stats.linregress(x, y)

    assert pytest.approx(summary.beta_1, abs=1e-8) == scipy_res.slope
    assert pytest.approx(summary.beta_0, abs=1e-8) == scipy_res.intercept
    assert pytest.approx(summary.se_beta_1, abs=1e-8) == scipy_res.stderr
    assert pytest.approx(summary.se_beta_0, abs=1e-8) == scipy_res.intercept_stderr
    assert pytest.approx(summary.r_squared, abs=1e-8) == scipy_res.rvalue ** 2
    assert pytest.approx(summary.p_val_beta_1, abs=1e-8) == scipy_res.pvalue
