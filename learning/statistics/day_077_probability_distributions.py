"""
Probability Distributions Implementation (Normal, Binomial, Poisson).

This module provides object-oriented implementations of three fundamental
probability distributions with analytical probability functions, cumulative
density/mass functions, summary statistics, and numerical calculations.
"""

import math
from typing import Dict


class NormalDistribution:
    """Continuous Normal (Gaussian) Distribution N(mu, sigma^2)."""

    def __init__(self, mean: float = 0.0, std_dev: float = 1.0) -> None:
        if std_dev <= 0:
            raise ValueError("Standard deviation must be strictly positive.")
        self.mean = float(mean)
        self.std_dev = float(std_dev)
        self.variance = self.std_dev ** 2

    def pdf(self, x: float) -> float:
        """Calculate Probability Density Function (PDF) at point x."""
        z = (x - self.mean) / self.std_dev
        return (1.0 / (self.std_dev * math.sqrt(2.0 * math.pi))) * math.exp(-0.5 * z * z)

    def cdf(self, x: float) -> float:
        """Calculate Cumulative Distribution Function (CDF) P(X <= x)."""
        z = (x - self.mean) / (self.std_dev * math.sqrt(2.0))
        return 0.5 * (1.0 + math.erf(z))

    def probability_range(self, low: float, high: float) -> float:
        """Calculate probability P(low <= X <= high)."""
        if low > high:
            raise ValueError("Lower bound must not exceed upper bound.")
        return self.cdf(high) - self.cdf(low)

    def summary(self) -> Dict[str, float]:
        """Return parameter statistics."""
        return {
            "mean": self.mean,
            "variance": self.variance,
            "std_dev": self.std_dev,
            "skewness": 0.0,
            "kurtosis": 0.0,
        }


class BinomialDistribution:
    """Discrete Binomial Distribution B(n, p)."""

    def __init__(self, trials: int, p: float) -> None:
        if not isinstance(trials, int) or trials < 0:
            raise ValueError("Number of trials 'n' must be a non-negative integer.")
        if not (0.0 <= p <= 1.0):
            raise ValueError("Probability 'p' must be between 0.0 and 1.0 inclusive.")
        self.trials = trials
        self.p = float(p)

    @property
    def mean(self) -> float:
        return self.trials * self.p

    @property
    def variance(self) -> float:
        return self.trials * self.p * (1.0 - self.p)

    def pmf(self, k: int) -> float:
        """Calculate Probability Mass Function (PMF) for k successes."""
        if not isinstance(k, int) or k < 0 or k > self.trials:
            return 0.0
        combinations = math.comb(self.trials, k)
        return combinations * (self.p ** k) * ((1.0 - self.p) ** (self.trials - k))

    def cdf(self, k: int) -> float:
        """Calculate Cumulative Distribution Function P(X <= k)."""
        if k < 0:
            return 0.0
        if k >= self.trials:
            return 1.0
        return sum(self.pmf(i) for i in range(k + 1))

    def summary(self) -> Dict[str, float]:
        """Return parameter statistics."""
        q = 1.0 - self.p
        skewness = (q - self.p) / math.sqrt(self.trials * self.p * q) if (self.trials > 0 and self.p > 0 and q > 0) else 0.0
        return {
            "trials": float(self.trials),
            "p": self.p,
            "mean": self.mean,
            "variance": self.variance,
            "skewness": skewness,
        }


class PoissonDistribution:
    """Discrete Poisson Distribution Pois(lambda)."""

    def __init__(self, rate: float) -> None:
        if rate <= 0:
            raise ValueError("Rate parameter 'rate' (lambda) must be strictly positive.")
        self.rate = float(rate)

    @property
    def mean(self) -> float:
        return self.rate

    @property
    def variance(self) -> float:
        return self.rate

    def pmf(self, k: int) -> float:
        """Calculate PMF for k events: P(X = k) = (lambda^k * e^-lambda) / k!."""
        if not isinstance(k, int) or k < 0:
            return 0.0
        log_pmf = k * math.log(self.rate) - self.rate - math.lgamma(k + 1)
        return math.exp(log_pmf)

    def cdf(self, k: int) -> float:
        """Calculate CDF P(X <= k)."""
        if k < 0:
            return 0.0
        return sum(self.pmf(i) for i in range(k + 1))

    def summary(self) -> Dict[str, float]:
        """Return parameter statistics."""
        return {
            "rate": self.rate,
            "mean": self.mean,
            "variance": self.variance,
            "skewness": 1.0 / math.sqrt(self.rate),
        }
