"""
Unit tests for Bayes Theorem and Conditional Probability implementation.
"""

import pytest
import numpy as np
from learning.statistics.day_089_bayes_theorem import (
    DiagnosticTestEvaluator,
    BayesianDiscreteUpdater,
    compute_bayes_factor
)


def test_diagnostic_test_evaluator_rare_disease():
    # Disease prevalence = 1% (0.01)
    # Sensitivity (P(T+|D)) = 99% (0.99)
    # Specificity (P(T-|D')) = 95% (0.95)
    evaluator = DiagnosticTestEvaluator(prevalence=0.01, sensitivity=0.99, specificity=0.95)

    ppv = evaluator.positive_predictive_value()
    # P(D|T+) = (0.99 * 0.01) / (0.99 * 0.01 + 0.05 * 0.99) = 0.0099 / (0.0099 + 0.0495) = 1/6 ~= 0.166666...
    assert pytest.approx(ppv, abs=1e-5) == 1 / 6

    npv = evaluator.negative_predictive_value()
    # P(D'|T-) = (0.95 * 0.99) / (0.95 * 0.99 + 0.01 * 0.01) = 0.9405 / 0.9406 ~= 0.9998937
    assert pytest.approx(npv, abs=1e-5) == 0.9405 / 0.9406

    assert evaluator.false_positive_rate() == pytest.approx(0.05)
    assert evaluator.false_negative_rate() == pytest.approx(0.01)


def test_diagnostic_test_invalid_inputs():
    with pytest.raises(ValueError):
        DiagnosticTestEvaluator(prevalence=1.5, sensitivity=0.9, specificity=0.9)


def test_bayesian_discrete_updater_coin_toss():
    # Hypothesis: H0 (Fair coin, P(H)=0.5), H1 (Biased coin, P(H)=0.75)
    hypotheses = ["Fair", "Biased"]
    priors = [0.5, 0.5]
    updater = BayesianDiscreteUpdater(hypotheses, priors)

    # 1st evidence: Head
    # Likelihoods: P(Head | Fair)=0.5, P(Head | Biased)=0.75
    p1 = updater.update([0.5, 0.75])
    # Posterior: Fair=0.4, Biased=0.6
    assert pytest.approx(p1[0]) == 0.4
    assert pytest.approx(p1[1]) == 0.6

    # 2nd evidence: Head
    p2 = updater.update([0.5, 0.75])
    # P2 = [0.4*0.5, 0.6*0.75] / 0.65 = [0.20/0.65, 0.45/0.65] = [4/13, 9/13]
    assert pytest.approx(p2[0]) == 4 / 13
    assert pytest.approx(p2[1]) == 9 / 13

    dist = updater.get_distribution()
    assert pytest.approx(dist["Fair"]) == 4 / 13
    assert pytest.approx(dist["Biased"]) == 9 / 13


def test_bayesian_updater_validation():
    with pytest.raises(ValueError):
        BayesianDiscreteUpdater(["H1", "H2"], [0.5])

    updater = BayesianDiscreteUpdater(["H1", "H2"], [0.5, 0.5])
    with pytest.raises(ValueError):
        updater.update([0.0, 0.0])  # Marginal evidence zero


def test_bayes_factor():
    # Prior H1=0.5, Prior H0=0.5 (Prior Odds = 1.0)
    # Posterior H1=0.75, Posterior H0=0.25 (Posterior Odds = 3.0)
    bf = compute_bayes_factor(0.5, 0.5, 0.75, 0.25)
    assert pytest.approx(bf) == 3.0
