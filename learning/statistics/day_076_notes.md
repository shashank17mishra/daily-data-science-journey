# Day 076: Descriptive Statistics: Mean, Std Dev, Variance

## Overview
Implementation of foundational descriptive statistics functions including mean, variance, standard deviation, standard error, percentile estimation, and online/streaming stats using Welford's algorithm.

## Objectives
- Understand practical application of Descriptive Statistics: Mean, Std Dev, Variance.
- Write executable verification tests.

## Key Concepts
Descriptive statistics provide quantitative summaries of a sample or population.

Key Concepts:
1. **Mean (Arithmetic Average)**: The sum of elements divided by sample count $N$.
2. **Variance**: Measures data dispersion around the mean.
   - **Sample Variance ($s^2$)**: Uses Bessel's correction ($N-1$ degrees of freedom, `ddof=1`) to yield an unbiased estimator of population variance.
   - **Population Variance ($

igma^2$)**: Uses $N$ (`ddof=0`).
3. **Standard Deviation ($s$ or $

igma$)**: Square root of variance, providing dispersion metrics in the original measurement units.
4. **Standard Error of the Mean (SEM)**: $s / \sqrt{N}$, estimating uncertainty around the sample mean.
5. **Percentiles & Interquartile Range (IQR)**: Ranked division of sorted data ($Q_3 - Q_1$) robust to outliers.
6. **Welford's Algorithm**: An online streaming method for computing running mean and variance in a single pass without catastrophic cancellation inherent in naive formulas.
