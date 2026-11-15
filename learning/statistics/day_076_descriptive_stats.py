"""Descriptive Statistics Computation Module.

Provides implementations for calculating central tendency, dispersion,
percentiles, and online streaming statistics using Welford's algorithm.
"""

from dataclasses import dataclass
import math
from typing import List


@dataclass
class StatsResult:
    """Summary of descriptive statistics for a dataset."""

    count: int
    mean: float
    variance: float
    std_dev: float
    sem: float
    min_val: float
    max_val: float
    median: float
    q1: float
    q3: float
    iqr: float


def compute_mean(data: List[float]) -> float:
    """Calculate arithmetic mean of a dataset."""
    if not data:
        raise ValueError("Cannot calculate mean of an empty dataset.")
    return sum(data) / len(data)


def compute_variance(data: List[float], ddof: int = 1) -> float:
    """Calculate variance with specified degrees of freedom.
    
    Use ddof=1 for sample variance, ddof=0 for population variance.
    """
    n = len(data)
    if n <= ddof:
        raise ValueError(
            f"Dataset length ({n}) must be greater than ddof ({ddof})."
        )
    mean_val = compute_mean(data)
    sum_sq_diff = sum((x - mean_val) ** 2 for x in data)
    return sum_sq_diff / (n - ddof)


def compute_std_dev(data: List[float], ddof: int = 1) -> float:
    """Calculate standard deviation."""
    return math.sqrt(compute_variance(data, ddof=ddof))


def compute_percentile(data: List[float], percentile: float) -> float:
    """Calculate specified percentile (0 to 100) using linear interpolation."""
    if not data:
        raise ValueError("Cannot calculate percentile of an empty dataset.")
    if not (0.0 <= percentile <= 100.0):
        raise ValueError("Percentile must be between 0 and 100.")

    sorted_data = sorted(data)
    n = len(sorted_data)
    if n == 1:
        return float(sorted_data[0])

    index = (n - 1) * (percentile / 100.0)
    lower = math.floor(index)
    upper = math.ceil(index)
    fraction = index - lower

    if lower == upper:
        return float(sorted_data[lower])
    return sorted_data[lower] + fraction * (
        sorted_data[upper] - sorted_data[lower]
    )


def compute_summary_stats(data: List[float], ddof: int = 1) -> StatsResult:
    """Compute comprehensive descriptive statistics for a dataset."""
    if not data:
        raise ValueError("Dataset cannot be empty.")
    n = len(data)
    mean_val = compute_mean(data)
    var_val = compute_variance(data, ddof=ddof)
    std_val = math.sqrt(var_val)
    sem_val = std_val / math.sqrt(n)

    min_v = float(min(data))
    max_v = float(max(data))
    median_v = compute_percentile(data, 50.0)
    q1_v = compute_percentile(data, 25.0)
    q3_v = compute_percentile(data, 75.0)
    iqr_v = q3_v - q1_v

    return StatsResult(
        count=n,
        mean=mean_val,
        variance=var_val,
        std_dev=std_val,
        sem=sem_val,
        min_val=min_v,
        max_val=max_v,
        median=median_v,
        q1=q1_v,
        q3=q3_v,
        iqr=iqr_v,
    )


class WelfordAccumulator:
    """Online/streaming algorithm for numerical stability in mean and variance."""

    def __init__(self) -> None:
        self.count: int = 0
        self.mean: float = 0.0
        self._m2: float = 0.0

    def update(self, x: float) -> None:
        """Update streaming statistics with a single data point."""
        self.count += 1
        delta = x - self.mean
        self.mean += delta / self.count
        delta2 = x - self.mean
        self._m2 += delta * delta2

    def variance(self, ddof: int = 1) -> float:
        """Calculate current variance given accumulated stream."""
        if self.count <= ddof:
            raise ValueError(
                f"Accumulated count ({self.count}) must be greater than ddof ({ddof})."
            )
        return self._m2 / (self.count - ddof)

    def std_dev(self, ddof: int = 1) -> float:
        """Calculate current standard deviation."""
        return math.sqrt(self.variance(ddof=ddof))

    def merge(self, other: "WelfordAccumulator") -> "WelfordAccumulator":
        """Combine statistics from two accumulators (Chan's algorithm)."""
        if self.count == 0:
            res = WelfordAccumulator()
            res.count, res.mean, res._m2 = other.count, other.mean, other._m2
            return res
        if other.count == 0:
            res = WelfordAccumulator()
            res.count, res.mean, res._m2 = self.count, self.mean, self._m2
            return res

        res = WelfordAccumulator()
        res.count = self.count + other.count
        delta = other.mean - self.mean
        res.mean = self.mean + delta * other.count / res.count
        res._m2 = (
            self._m2
            + other._m2
            + (delta**2) * self.count * other.count / res.count
        )
        return res
