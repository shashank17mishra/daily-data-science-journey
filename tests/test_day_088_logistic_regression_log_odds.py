import numpy as np
import pytest
from learning.statistics.day_088_logistic_regression_log_odds import (
    sigmoid,
    logit,
    LogisticRegressionLogOdds,
)


def test_sigmoid_values():
    assert np.isclose(sigmoid(0.0), 0.5)
    assert sigmoid(100.0) > 0.9999
    assert sigmoid(-100.0) < 0.0001
    # Test vector input
    arr = np.array([-10.0, 0.0, 10.0])
    res = sigmoid(arr)
    assert res.shape == (3,)
    assert res[0] < res[1] < res[2]


def test_logit_inverse_of_sigmoid():
    z_values = np.array([-3.0, -1.0, 0.0, 1.5, 4.0])
    probs = sigmoid(z_values)
    reconstructed_z = logit(probs)
    np.testing.assert_allclose(z_values, reconstructed_z, rtol=1e-5, atol=1e-5)


def test_model_unfitted_raises():
    model = LogisticRegressionLogOdds()
    X = np.array([[1.0, 2.0]])
    with pytest.raises(ValueError):
        model.predict_log_odds(X)
    with pytest.raises(ValueError):
        model.odds_ratios()


def test_model_fit_linearly_separable():
    np.random.seed(42)
    # Class 0 centered around (-2, -2), Class 1 centered around (2, 2)
    X0 = np.random.randn(50, 2) - 2.0
    X1 = np.random.randn(50, 2) + 2.0
    X = np.vstack([X0, X1])
    y = np.hstack([np.zeros(50), np.ones(50)])

    model = LogisticRegressionLogOdds(learning_rate=0.5, max_iter=500)
    model.fit(X, y)

    # Verify loss decreases monotonically or converges
    assert len(model.loss_history) > 1
    assert model.loss_history[-1] < model.loss_history[0]

    # Predict binary labels
    preds = model.predict(X)
    accuracy = np.mean(preds == y)
    assert accuracy > 0.95


def test_log_odds_and_probability_consistency():
    X = np.array([[1.0, 0.5], [-1.0, -0.5], [2.0, 1.0]])
    y = np.array([1, 0, 1])

    model = LogisticRegressionLogOdds(learning_rate=0.1, max_iter=100)
    model.fit(X, y)

    log_odds = model.predict_log_odds(X)
    probs = model.predict_proba(X)

    # Probabilities should equal sigmoid(log_odds)
    np.testing.assert_allclose(probs, sigmoid(log_odds))


def test_odds_ratios_calculation():
    model = LogisticRegressionLogOdds()
    model.weights = np.array([0.0, np.log(2.0), np.log(0.5)])
    ors = model.odds_ratios()
    expected = np.array([1.0, 2.0, 0.5])
    np.testing.assert_allclose(ors, expected, rtol=1e-5)
