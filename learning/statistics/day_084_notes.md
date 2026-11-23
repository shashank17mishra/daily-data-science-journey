# Day 084: Pearson & Spearman Correlation Analysis

## Overview
Implementation of Pearson linear correlation and Spearman rank correlation from scratch, including tie-handling rank computation, Fisher z-transformation confidence intervals, statistical significance testing, and structural relationship comparison.

## Objectives
- Understand practical application of Pearson & Spearman Correlation.
- Write executable verification tests.

## Key Concepts
This exercise implements Pearson's linear correlation coefficient ($r$) and Spearman's rank correlation coefficient ($\rho$) from foundational principles.

Key Concepts:
1. **Pearson Correlation ($r$)**: Measures the linear relationship between two continuous variables. It is computed as the covariance normalized by the product of standard deviations. Confidence intervals are calculated using Fisher's $z$-transformation ($z = \text{atanh}(r)$), where $z \sim \mathcal{N}(z, 1/\sqrt{n-3})$.
2. **Spearman Correlation ($\rho$)**: Evaluates non-linear, monotonic relationships by transforming raw numeric values into fractional ranks (with average rank assignments for tied elements) and computing Pearson correlation on those ranks.
3. **Comparative Diagnostics**: By comparing $|\rho|$ with $|r|$, the `BivariateCorrelationAnalyzer` detects strong non-linear monotonic trends or extreme outlier sensitivity.
