import pytest
import numpy as np
from learning.statistics.day_087_multiple_linear_regression_multicollinearity import (
    MultipleLinearRegression,
    calculate_vif,
    condition_number,
    stepwise_vif_pruning,
)


def test_regression_exact_fit():
    np.random.seed(42)
    X = np.random.randn(100, 3)
    true_beta = np.array([1.5, -2.0, 0.5])
    true_intercept = 4.0
    y = X @ true_beta + true_intercept

    model = MultipleLinearRegression(fit_intercept=True)
    model.fit(X, y)

    np.testing.assert_allclose(model.coefficients, true_beta, rtol=1e-5, atol=1e-5)
    assert pytest.approx(model.intercept, abs=1e-5) == true_intercept
    assert pytest.approx(model.r_squared, abs=1e-5) == 1.0

    preds = model.predict(X)
    np.testing.assert_allclose(preds, y, rtol=1e-5, atol=1e-5)


def test_regression_no_intercept():
    np.random.seed(42)
    X = np.random.randn(50, 2)
    true_beta = np.array([3.0, -1.0])
    y = X @ true_beta

    model = MultipleLinearRegression(fit_intercept=False)
    model.fit(X, y)

    np.testing.assert_allclose(model.coefficients, true_beta, rtol=1e-5, atol=1e-5)
    assert model.intercept == 0.0


def test_vif_calculation_collinear_features():
    np.random.seed(42)
    x0 = np.random.randn(100)
    x1 = np.random.randn(100)
    x2 = 2.0 * x0 + np.random.randn(100) * 0.001

    X = np.column_stack([x0, x1, x2])
    vifs = calculate_vif(X)

    assert vifs[0] > 10.0
    assert vifs[2] > 10.0
    assert vifs[1] < 2.0


def test_stepwise_vif_pruning():
    np.random.seed(42)
    x0 = np.random.randn(100)
    x1 = np.random.randn(100)
    x2 = 3.0 * x0 + np.random.randn(100) * 0.0001

    X = np.column_stack([x0, x1, x2])
    feature_names = ["feat_0", "feat_1", "feat_2"]

    X_pruned, kept_names, kept_indices = stepwise_vif_pruning(
        X, threshold=5.0, feature_names=feature_names
    )

    assert len(kept_indices) == 2
    assert "feat_1" in kept_names
    assert ("feat_0" in kept_names) != ("feat_2" in kept_names)
    assert X_pruned.shape[1] == 2


def test_condition_number():
    X_independent = np.eye(4)
    cond_indep = condition_number(X_independent)
    assert pytest.approx(cond_indep, abs=1e-5) == 1.0

    np.random.seed(42)
    col1 = np.random.randn(50)
    col2 = col1 * 1.000001
    X_collinear = np.column_stack([col1, col2])
    cond_collinear = condition_number(X_collinear)

    assert cond_collinear > 1e4


def test_model_summary_structure():
    np.random.seed(42)
    X = np.random.randn(30, 2)
    y = 2 * X[:, 0] + np.random.randn(30) * 0.1

    model = MultipleLinearRegression(fit_intercept=True)
    model.fit(X, y, feature_names=["f1", "f2"])
    summary = model.summary()

    assert "r_squared" in summary
    assert "adj_r_squared" in summary
    assert "coefficients" in summary
    assert "f1" in summary["coefficients"]
    assert "f2" in summary["coefficients"]
    assert "p_value" in summary["coefficients"]["f1"]


def test_unfitted_model_errors():
    model = MultipleLinearRegression()
    X = np.array([[1.0, 2.0]])

    with pytest.raises(RuntimeError):
        model.predict(X)

    with pytest.raises(RuntimeError):
        model.summary()


def test_insufficient_samples_error():
    X = np.array([[1.0, 2.0], [3.0, 4.0]])
    y = np.array([1.0, 2.0])

    model = MultipleLinearRegression(fit_intercept=True)
    with pytest.raises(ValueError, match="Degrees of freedom must be > 0"):
        model.fit(X, y)
