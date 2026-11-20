# Day 081: Hypothesis Testing: Two-Sample t-Test

## Overview
Implement robust two-sample t-tests (Student's t-test and Welch's t-test) from scratch using NumPy and SciPy, including p-value calculation, degrees of freedom estimation via Welch-Satterthwaite equation, confidence intervals, and paired t-tests.

## Objectives
- Understand practical application of Hypothesis Testing: Two-Sample t-Test.
- Implement Welch's t-test and Student's t-test with proper degrees of freedom.
- Write executable verification tests using pytest.

## Key Concepts
This exercise covers hypothesis testing for two samples. Welch's t-test is more robust when population variances and sample sizes differ because it does not assume homogeneity of variance and computes fractional degrees of freedom via the Welch-Satterthwaite equation. Student's t-test assumes equal variances and pools sample variances together. Paired t-tests account for dependent paired observations by analyzing within-subject differences.
