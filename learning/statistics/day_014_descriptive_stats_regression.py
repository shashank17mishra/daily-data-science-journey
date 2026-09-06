"""
Day 014: Descriptive Statistics & Simple Linear Regression (Ordinary Least Squares).
"""
import math
from typing import List, Tuple

def compute_mean_and_variance(data: List[float]) -> Tuple[float, float]:
    """Calculates sample mean and sample variance of a dataset."""
    n = len(data)
    if n < 2:
        raise ValueError("Variance requires at least two data points.")

    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / (n - 1)
    return round(mean, 4), round(variance, 4)

def fit_simple_linear_regression(x: List[float], y: List[float]) -> Tuple[float, float, float]:
    """
    Fits Ordinary Least Squares (OLS) simple linear regression: y = beta_0 + beta_1 * x
    Returns: (beta_0 [intercept], beta_1 [slope], r_squared)
    """
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("X and Y must be non-empty lists of equal length (>= 2).")

    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = sum((x[i] - mean_x) ** 2 for i in range(n))

    if denominator == 0:
        raise ValueError("Variance of X is zero; cannot compute slope.")

    slope = numerator / denominator
    intercept = mean_y - (slope * mean_x)

    # Calculate R-squared
    ss_tot = sum((y[i] - mean_y) ** 2 for i in range(n))
    y_pred = [intercept + slope * x[i] for i in range(n)]
    ss_res = sum((y[i] - y_pred[i]) ** 2 for i in range(n))

    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 0.0

    return round(intercept, 4), round(slope, 4), round(r_squared, 4)
