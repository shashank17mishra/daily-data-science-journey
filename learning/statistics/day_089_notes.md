# Day 089: Bayes Theorem & Conditional Probability

## Overview
Implement a Python framework for Bayesian inference, diagnostic test evaluation (sensitivity, specificity, PPV, NPV), sequential evidence updating across discrete hypotheses, and Bayes factor calculation.

## Objectives
- Understand practical application of Bayes Theorem & Conditional Probability.
- Write executable verification tests.

## Key Concepts
Bayes' Theorem provides the mathematical framework for updating probabilities based on observed evidence:

$$P(H | E) = \frac{P(E | H) P(H)}{P(E)}$$

Where:
- $P(H)$ is the Prior probability of the hypothesis.
- $P(E | H)$ is the Likelihood of observing evidence $E$ given hypothesis $H$.
- $P(E) = \sum_i P(E | H_i) P(H_i)$ is the Marginal Likelihood (or Evidence).
- $P(H | E)$ is the Posterior probability.

In medical diagnostic testing:
- Positive Predictive Value (PPV) is $P(\text{Disease} | \text{Test}+)$. Even with high sensitivity and specificity, rare diseases (low prior prevalence) yield surprisingly low PPVs due to false positives from the large non-diseased population.
- Negative Predictive Value (NPV) is $P(\text{No Disease} | \text{Test}-)$.

Sequential Bayesian Updating uses the posterior distribution of step $k$ as the prior distribution for step $k+1$, accumulating evidence dynamically.

The Bayes Factor $BF_{10}$ quantifies evidence strength in favor of hypothesis $H_1$ relative to baseline hypothesis $H_0$, computed as the ratio of posterior odds to prior odds.
