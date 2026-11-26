# Day 087: Multiple Linear Regression & Multicollinearity

## Overview
Implements Multiple Linear Regression via Ordinary Least Squares (OLS) from scratch alongside essential multicollinearity diagnostics including Variance Inflation Factor (VIF), Matrix Condition Number, and Stepwise VIF Feature Pruning.

## Objectives
- Understand practical application of Multiple Linear Regression & Multicollinearity.
- Write executable verification tests.

## Key Concepts
This exercise implements Ordinary Least Squares (OLS) Multiple Linear Regression and diagnostics for Multicollinearity.

1. OLS Parameter Estimation: Estimates coefficient vector beta using normal equations via pseudo-inverse: beta = pinv(X^T X) X^T y. Standard errors, t-statistics, and two-sided p-values are computed from the variance-covariance matrix of beta.
2. Multicollinearity Diagnostics:
   - Variance Inflation Factor (VIF): Quantifies how much variance of an estimated regression coefficient is inflated due to collinearity. For feature j, VIF_j = 1 / (1 - R_j^2), where R_j^2 is the R-squared from regressing feature j against all other features.
   - Condition Number: Ratio of the largest to smallest singular value of X. High condition numbers (> 30) signal severe multicollinearity.
3. Stepwise VIF Feature Selection: Iteratively removes features with the highest VIF exceeding a specified threshold until all remaining features satisfy the threshold constraint.
