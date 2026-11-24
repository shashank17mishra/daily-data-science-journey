# Day 085: Covariance & Covariance Matrix

## Overview
Implementation of sample/population covariance, multi-dimensional covariance matrix computation from scratch, conversion to correlation matrices, Mahalanobis distance for multivariate outlier detection, and covariance-based Principal Component Analysis (PCA).

## Objectives
- Understand practical application of Covariance & Covariance Matrix.
- Write executable verification tests.

## Key Concepts
Covariance measures how two variables co-vary jointly around their respective means. For multi-dimensional data with N samples and D features, the D x D covariance matrix captures all pairwise feature covariances along its off-diagonals and feature variances along its diagonal. In matrix notation, given mean-centered data matrix X (shape N x D), the covariance matrix is computed as Cov(X) = (X^T @ X) / (N - ddof).

Key applications built upon the covariance matrix:
1. Standardisation to Correlation: Dividing covariance elements by the product of individual standard deviations standardizes covariance values to the [-1, 1] range.
2. Mahalanobis Distance: Measures distance scaled by the distribution's covariance matrix, accounting for correlation and scale differences between dimensions: d_M(x, mu) = sqrt((x - mu)^T * Sigma^-1 * (x - mu)).
3. Principal Component Analysis (PCA): Eigen-decomposition of the covariance matrix yields eigenvectors representing directions of maximum variance (principal axes) and eigenvalues representing variance magnitude along those axes.
