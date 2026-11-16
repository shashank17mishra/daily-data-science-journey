# Day 077: Probability Distributions: Normal, Binomial, Poisson

## Overview
Implement standard parametric probability distributions (Normal, Binomial, and Poisson) from scratch using mathematical principles. Compute probability density/mass functions (PDF/PMF), cumulative distribution functions (CDF), range probabilities, and summary statistics.

## Objectives
- Understand practical application of Probability Distributions: Normal, Binomial, Poisson.
- Write executable verification tests.

## Key Concepts
This exercise implements three fundamental theoretical probability distributions using clean Python math functions:

1. **Normal Distribution ($N(\mu, \sigma^2)$)**: Continuous distribution used for modeling natural phenomena. The CDF is implemented using standard error function `math.erf` via the standard identity $F(x) = \frac{1}{2} [1 + \text{erf}(\frac{x - \mu}{\sigma \sqrt{2}})]$.
2. **Binomial Distribution ($B(n, p)$)**: Discrete probability distribution modeling the number of successes in $n$ independent Bernoulli trials. Uses `math.comb` for calculating binomial coefficients.
3. **Poisson Distribution ($Pois(\lambda)$)**: Discrete distribution modeling arrival counts in fixed time intervals. Implemented using logarithmic scale computations via `math.lgamma(k + 1)` for high precision and numerical stability against factorial overflow.
