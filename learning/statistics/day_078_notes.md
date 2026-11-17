# Day 078: Central Limit Theorem & Sampling

## Overview
Implement a Python module to demonstrate the Central Limit Theorem (CLT) via Monte Carlo sampling from non-normal distributions (e.g., Exponential distribution), and provide pytest tests verifying sample mean normality.

## Objectives
- Understand practical application of Central Limit Theorem & Sampling.
- Write executable verification tests for sample mean distributions.

## Key Concepts
The Central Limit Theorem (CLT) states that the distribution of sample means approximates a normal distribution as the sample size gets larger, regardless of the population's underlying distribution. This exercise implements a Monte Carlo simulation framework to sample from skewed (exponential) and bounded uniform distributions, verifying both the expected value and the standard error scaling (pop_std / sqrt(n)).
