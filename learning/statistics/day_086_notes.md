# Day 086: Simple Linear Regression Theory & Practical OLS Implementation

## Overview
Mathematical implementation and statistical inference for Simple Linear Regression from first principles using Ordinary Least Squares (OLS), including parameter estimation, ANOVA decomposition, hypothesis testing (t-tests and F-test), confidence intervals, and prediction intervals.

## Objectives
- Understand practical application of Simple Linear Regression Theory.
- Write executable verification tests.

## Key Concepts
Simple Linear Regression models a linear relation between a continuous explanatory variable X and a continuous response Y using the model Y = \beta_0 + \beta_1 X + \epsilon. Under the Gauss-Markov assumptions (uncorrelated errors with zero mean and constant variance \sigma^2), the Ordinary Least Squares (OLS) estimators \hat{\beta}_1 = S_{xy} / S_{xx} and \hat{\beta}_0 = \bar{y} - \hat{\beta}_1 \bar{x} are the Best Linear Unbiased Estimators (BLUE).

Key Statistical Concepts Implemented:
1. Parameter Standard Errors: Derivation of sampling variance for slope SE(\hat{\beta}_1) = \sqrt{MSE / S_{xx}} and intercept SE(\hat{\beta}_0) = \sqrt{MSE (1/n + \bar{x}^2 / S_{xx})}.
2. Hypothesis Testing & Summary Statistics: Student's t-test for testing H_0: \beta_j = 0 and ANOVA F-test for overall model significance.
3. Confidence Interval vs. Prediction Interval:
   - Confidence Interval for Mean Response E[Y|X=x_0]: Accounts for estimation uncertainty in \hat{\beta}_0 and \hat{\beta}_1.
   - Prediction Interval for New Single Observation Y_0: Accounts for both model parameter estimation error AND the inherent noise variability \sigma^2 of individual future observations, making prediction intervals strictly wider.
