# Day 088: Logistic Regression Log-Odds & Sigmoid

## Overview
Implementation of Logistic Regression from scratch focusing on the mathematical relationship between linear decision boundaries, log-odds (logit), probability transformations via the sigmoid function, and feature odds ratios.

## Objectives
- Understand practical application of Logistic Regression Log-Odds & Sigmoid.
- Write executable verification tests.

## Key Concepts
Logistic regression is a fundamental generalized linear model (GLM) for binary classification. Unlike linear regression which predicts continuous outcomes directly, logistic regression models the log-odds (logit) of the binary outcome as a linear combination of input features:

$$\text{logit}(P(Y=1|X)) = \ln\left(\frac{P(Y=1|X)}{1 - P(Y=1|X)}\right) = Xw + b$$

Applying the inverse of the logit function—the standard logistic function (sigmoid)—maps any real number $z = Xw + b$ into a probability range $[0, 1]$:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

Key Concepts Implemented:
1. **Numerically Stable Sigmoid**: Computed via piecewise conditions to prevent overflow when evaluating $e^{-z}$ for large negative $z$.
2. **Logit Transformation**: Converts probabilities back to linear log-odds scale, safely clipping values to prevent division by zero or $\ln(0)$.
3. **Odds Ratio**: $e^{w_i}$ represents how the odds of $Y=1$ scale with a one-unit increase in feature $x_i$. An odds ratio $>1$ indicates positive association, while $<1$ indicates negative association.
