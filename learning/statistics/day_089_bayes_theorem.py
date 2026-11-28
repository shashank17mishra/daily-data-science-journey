"""
Day 089: Bayes Theorem & Conditional Probability

This module implements a framework for Bayesian inference, conditional probability updates,
diagnostic test evaluation (sensitivity, specificity, prevalence), sequential updating,
and hypothesis comparison using Bayes Factors.
"""

from typing import Dict, List
import numpy as np


class DiagnosticTestEvaluator:
    """Evaluates diagnostic test performance and updates disease probabilities using Bayes' Theorem."""

    def __init__(self, prevalence: float, sensitivity: float, specificity: float):
        """
        Initialize diagnostic test parameters.

        Args:
            prevalence: Prior probability of disease P(D)
            sensitivity: True positive rate P(T+|D)
            specificity: True negative rate P(T-|D')
        """
        if not (0 <= prevalence <= 1 and 0 <= sensitivity <= 1 and 0 <= specificity <= 1):
            raise ValueError("Probabilities must be between 0 and 1.")

        self.prevalence = float(prevalence)
        self.sensitivity = float(sensitivity)
        self.specificity = float(specificity)

    def positive_predictive_value(self) -> float:
        """
        Calculate P(D|T+): Posterior probability of disease given a positive test.
        Bayes' Theorem: P(D|T+) = P(T+|D) * P(D) / [P(T+|D)*P(D) + P(T+|D')*P(D')]
        """
        p_d = self.prevalence
        p_not_d = 1.0 - p_d
        p_pos_given_d = self.sensitivity
        p_pos_given_not_d = 1.0 - self.specificity

        marginal_pos = (p_pos_given_d * p_d) + (p_pos_given_not_d * p_not_d)
        if marginal_pos == 0:
            return 0.0
        return (p_pos_given_d * p_d) / marginal_pos

    def negative_predictive_value(self) -> float:
        """
        Calculate P(D'|T-): Posterior probability of NO disease given a negative test.
        Bayes' Theorem: P(D'|T-) = P(T-|D') * P(D') / [P(T-|D')*P(D') + P(T-|D)*P(D)]
        """
        p_d = self.prevalence
        p_not_d = 1.0 - p_d
        p_neg_given_not_d = self.specificity
        p_neg_given_d = 1.0 - self.sensitivity

        marginal_neg = (p_neg_given_not_d * p_not_d) + (p_neg_given_d * p_d)
        if marginal_neg == 0:
            return 0.0
        return (p_neg_given_not_d * p_not_d) / marginal_neg

    def false_positive_rate(self) -> float:
        """Calculate 1 - Specificity = P(T+|D')."""
        return 1.0 - self.specificity

    def false_negative_rate(self) -> float:
        """Calculate 1 - Sensitivity = P(T-|D)."""
        return 1.0 - self.sensitivity


class BayesianDiscreteUpdater:
    """
    Performs Bayesian updating across multiple mutually exclusive and exhaustive hypotheses.
    """

    def __init__(self, hypotheses: List[str], priors: List[float]):
        """
        Initialize prior distribution over hypotheses.

        Args:
            hypotheses: Names of hypotheses [H1, H2, ...]
            priors: Prior probabilities for each hypothesis. Must sum to 1.
        """
        if len(hypotheses) != len(priors):
            raise ValueError("Hypotheses and priors must have equal lengths.")

        priors_arr = np.array(priors, dtype=np.float64)
        if np.any(priors_arr < 0):
            raise ValueError("Prior probabilities cannot be negative.")

        total_prior = np.sum(priors_arr)
        if total_prior <= 0:
            raise ValueError("Sum of priors must be positive.")
        if not np.isclose(total_prior, 1.0):
            priors_arr = priors_arr / total_prior

        self.hypotheses = list(hypotheses)
        self.priors = priors_arr

    def update(self, likelihoods: List[float]) -> np.ndarray:
        """
        Update hypothesis probabilities given likelihoods P(Evidence | Hi).

        Args:
            likelihoods: Conditional probability of the evidence given each hypothesis.

        Returns:
            np.ndarray: Posterior probabilities P(Hi | Evidence).
        """
        likelihoods_arr = np.array(likelihoods, dtype=np.float64)
        if len(likelihoods_arr) != len(self.hypotheses):
            raise ValueError("Likelihoods count must match hypotheses count.")
        if np.any(likelihoods_arr < 0):
            raise ValueError("Likelihoods cannot be negative.")

        unnormalized_posteriors = self.priors * likelihoods_arr
        marginal_evidence = np.sum(unnormalized_posteriors)

        if marginal_evidence == 0:
            raise ValueError("Marginal evidence is zero; observation is impossible.")

        posteriors = unnormalized_posteriors / marginal_evidence
        self.priors = posteriors.copy()
        return posteriors

    def get_distribution(self) -> Dict[str, float]:
        """Return current probability distribution as a dictionary."""
        return dict(zip(self.hypotheses, self.priors))


def compute_bayes_factor(prior_h1: float, prior_h0: float, posterior_h1: float, posterior_h0: float) -> float:
    """
    Compute Bayes Factor BF_10 in favor of Hypothesis 1 over Hypothesis 0.
    BF_10 = (Posterior Odds) / (Prior Odds)

    Args:
        prior_h1: Prior probability of H1
        prior_h0: Prior probability of H0
        posterior_h1: Posterior probability of H1
        posterior_h0: Posterior probability of H0

    Returns:
        float: Bayes Factor BF_10
    """
    if prior_h1 <= 0 or prior_h0 <= 0:
        raise ValueError("Priors must be greater than zero.")
    if posterior_h0 == 0 or prior_h0 == 0:
        raise ValueError("Division by zero in Bayes Factor calculation.")

    prior_odds = prior_h1 / prior_h0
    posterior_odds = posterior_h1 / posterior_h0
    return float(posterior_odds / prior_odds)
