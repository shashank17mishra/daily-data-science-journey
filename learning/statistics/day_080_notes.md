# Day 080: Hypothesis Testing: Z-Test & One-Sample t-Test

## Overview
Implementation of Z-test and One-Sample t-test from scratch with support for custom significance levels, directional alternative hypotheses (two-sided, greater, less), and confidence interval calculation.

## Objectives
- Understand practical application of Hypothesis Testing: Z-Test & One-Sample t-Test.
- Write executable verification tests.

## Key Concepts
Hypothesis testing allows statistical inference on sample metrics against target population parameters.

Key Concepts:
1. Z-Test: Applied when the population standard deviation ($
sigma$) is known or sample size is very large. Uses standard normal $N(0,1)$ distribution for critical values and p-values.
2. One-Sample t-Test: Applied when population standard deviation ($
sigma$) is unknown and estimated from the sample standard deviation ($s$). Uses Student's t-distribution with $df = n - 1$.
3. Alternative Hypotheses:
   - Two-sided ($H_1: \mu \neq \mu_0$)
   - Greater / One-sided upper ($H_1: \mu > \mu_0$)
   - Less / One-sided lower ($H_1: \mu < \mu_0$)
4. Directional logic in tests: When sample mean $\bar{x} > \mu_0$, tests targeting `alternative='greater'` reject the null hypothesis ($p < \alpha$), while `alternative='less'` fails to reject ($p > 0.5$).
