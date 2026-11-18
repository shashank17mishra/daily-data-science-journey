# Day 079: Confidence Intervals & Estimation

## Overview
Implementation of core statistical estimation techniques including Parametric (Z and Student's t), Binomial Proportion (Wald and Wilson Score), Two-Sample Difference of Means, and Non-Parametric Bootstrap Confidence Intervals.

## Objectives
- Understand practical application of Confidence Intervals & Estimation.
- Write executable verification tests.

## Key Concepts
Confidence intervals (CIs) quantify the uncertainty associated with sample estimates. This implementation covers four key CI techniques:

1. **Parametric Mean Estimation**: Computes single-sample mean intervals using either Z-critical values (when population standard deviation is known) or Student's t-critical values (when standard deviation is estimated from sample variance with $n-1$ degrees of freedom).
2. **Binomial Proportion Estimation**: Implements both the classic **Wald interval** ($\hat{p} \pm z \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$) and the more robust **Wilson Score interval**, which performs significantly better for small sample sizes or proportions near 0 or 1.
3. **Difference of Means Interval**: Computes two-sample confidence intervals for mean differences ($m_1 - m_2$) under both equal variance assumptions (Pooled $t$) and unequal variance assumptions using the **Welch-Satterthwaite** effective degrees of freedom approximation.
4. **Non-Parametric Bootstrap Interval**: Draws repeated samples with replacement to estimate empirical percentile confidence intervals without assuming underlying normality, supporting custom statistical functions like median or skewness.
