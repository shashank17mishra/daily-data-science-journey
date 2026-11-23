"""
Day 084: Pearson & Spearman Correlation Analysis Engine
Implements robust statistical functions for bivariate correlation, rank transformation with tie handling,
Fisher z-transform confidence intervals, and hypothesis testing.
"""

import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import scipy.stats as stats


@dataclass
class CorrelationResult:
    statistic: float
    p_value: float
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None
    sample_size: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "statistic": self.statistic,
            "p_value": self.p_value,
            "ci_lower": self.ci_lower,
            "ci_upper": self.ci_upper,
            "sample_size": self.sample_size
        }


def compute_ranks(data: List[float]) -> List[float]:
    """
    Computes fractional ranks for a sequence of numeric values with tie handling (average rank).
    """
    n = len(data)
    indexed = sorted(enumerate(data), key=lambda x: x[1])
    ranks = [0.0] * n

    i = 0
    while i < n:
        j = i
        while j < n - 1 and indexed[j + 1][1] == indexed[i][1]:
            j += 1
        avg_rank = (i + j + 2) / 2.0
        for k in range(i, j + 1):
            original_idx = indexed[k][0]
            ranks[original_idx] = avg_rank
        i = j + 1

    return ranks


def calculate_pearson(
    x: List[float],
    y: List[float],
    alpha: float = 0.05
) -> CorrelationResult:
    """
    Calculates Pearson's correlation coefficient (r), p-value, and Fisher z-transformed CI.
    """
    if len(x) != len(y):
        raise ValueError("Input vectors x and y must have equal length.")

    n = len(x)
    if n < 3:
        raise ValueError("Sample size must be at least 3 for correlation analysis.")

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    var_x = sum((xi - mean_x) ** 2 for xi in x)
    var_y = sum((yi - mean_y) ** 2 for yi in y)

    if var_x == 0.0 or var_y == 0.0:
        raise ValueError("Variance of x or y is zero; correlation is undefined for constant arrays.")

    r = cov_xy / math.sqrt(var_x * var_y)
    r = max(-1.0, min(1.0, r))

    if abs(r) == 1.0:
        p_val = 0.0
        ci_low, ci_high = r, r
    else:
        df = n - 2
        t_stat = r * math.sqrt(df / (1.0 - r ** 2))
        p_val = 2.0 * (1.0 - stats.t.cdf(abs(t_stat), df))

        z = math.atanh(r)
        se_z = 1.0 / math.sqrt(n - 3)
        z_crit = stats.norm.ppf(1.0 - alpha / 2.0)
        z_low = z - z_crit * se_z
        z_high = z + z_crit * se_z
        ci_low = math.tanh(z_low)
        ci_high = math.tanh(z_high)

    return CorrelationResult(
        statistic=r,
        p_value=p_val,
        ci_lower=ci_low,
        ci_upper=ci_high,
        sample_size=n
    )


def calculate_spearman(x: List[float], y: List[float]) -> CorrelationResult:
    """
    Calculates Spearman's rank correlation coefficient (rho) and p-value.
    """
    if len(x) != len(y):
        raise ValueError("Input vectors x and y must have equal length.")

    n = len(x)
    if n < 3:
        raise ValueError("Sample size must be at least 3 for correlation analysis.")

    rank_x = compute_ranks(x)
    rank_y = compute_ranks(y)

    pearson_res = calculate_pearson(rank_x, rank_y)

    return CorrelationResult(
        statistic=pearson_res.statistic,
        p_value=pearson_res.p_value,
        ci_lower=None,
        ci_upper=None,
        sample_size=n
    )


class BivariateCorrelationAnalyzer:
    """
    Engine for comparative bivariate correlation analysis (Pearson vs Spearman).
    """

    def __init__(self, x: List[float], y: List[float]):
        if len(x) != len(y):
            raise ValueError("Input vectors x and y must have equal length.")
        self.x = list(x)
        self.y = list(y)

    def analyze(self) -> Dict[str, Any]:
        """
        Computes Pearson and Spearman correlations and identifies non-linear monotonic patterns.
        """
        pearson_res = calculate_pearson(self.x, self.y)
        spearman_res = calculate_spearman(self.x, self.y)

        diff = abs(spearman_res.statistic) - abs(pearson_res.statistic)
        is_non_linear_monotonic = diff > 0.1

        return {
            "pearson": pearson_res.to_dict(),
            "spearman": spearman_res.to_dict(),
            "abs_difference": diff,
            "non_linear_monotonic_trend": is_non_linear_monotonic
        }
