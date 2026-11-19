"""Day 080: Hypothesis Testing - Z-Test & One-Sample t-Test implementation."""

import math
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union
import numpy as np
from scipy import stats


@dataclass
class HypothesisTestResult:
    """Container for hypothesis test outcomes."""
    statistic: float
    p_value: float
    degrees_of_freedom: Optional[int]
    confidence_interval: Tuple[float, float]
    alpha: float
    alternative: str
    reject_null: bool


def z_test(
    data: Union[List[float], np.ndarray],
    pop_mean: float,
    pop_std: float,
    alpha: float = 0.05,
    alternative: str = "two-sided"
) -> HypothesisTestResult:
    """Perform a One-Sample Z-Test when population standard deviation is known.

    Args:
        data: Sample observations.
        pop_mean: Null hypothesis population mean (mu_0).
        pop_std: Known population standard deviation (sigma > 0).
        alpha: Significance level (0 < alpha < 1).
        alternative: Directional hypothesis ('two-sided', 'greater', 'less').

    Returns:
        HypothesisTestResult containing statistics, p-value, CI, and decision.
    """
    arr = np.asarray(data, dtype=float)
    if arr.size == 0:
        raise ValueError("Data array must not be empty.")
    if pop_std <= 0:
        raise ValueError("Population standard deviation pop_std must be positive.")
    if not (0 < alpha < 1):
        raise ValueError("Alpha must be strictly between 0 and 1.")
    if alternative not in ("two-sided", "greater", "less"):
        raise ValueError("Alternative must be 'two-sided', 'greater', or 'less'.")

    n = arr.size
    sample_mean = float(np.mean(arr))
    sem = pop_std / math.sqrt(n)
    z_stat = (sample_mean - pop_mean) / sem

    if alternative == "two-sided":
        p_val = 2.0 * float(stats.norm.sf(abs(z_stat)))
        z_crit = float(stats.norm.ppf(1.0 - alpha / 2.0))
        ci = (sample_mean - z_crit * sem, sample_mean + z_crit * sem)
    elif alternative == "greater":
        p_val = float(stats.norm.sf(z_stat))
        z_crit = float(stats.norm.ppf(1.0 - alpha))
        ci = (sample_mean - z_crit * sem, float("inf"))
    else:  # 'less'
        p_val = float(stats.norm.cdf(z_stat))
        z_crit = float(stats.norm.ppf(1.0 - alpha))
        ci = (float("-inf"), sample_mean + z_crit * sem)

    reject_null = bool(p_val < alpha)

    return HypothesisTestResult(
        statistic=z_stat,
        p_value=p_val,
        degrees_of_freedom=None,
        confidence_interval=ci,
        alpha=alpha,
        alternative=alternative,
        reject_null=reject_null
    )


def one_sample_t_test(
    data: Union[List[float], np.ndarray],
    pop_mean: float,
    alpha: float = 0.05,
    alternative: str = "two-sided"
) -> HypothesisTestResult:
    """Perform a One-Sample t-Test when population standard deviation is unknown.

    Args:
        data: Sample observations (n >= 2).
        pop_mean: Null hypothesis population mean (mu_0).
        alpha: Significance level (0 < alpha < 1).
        alternative: Directional hypothesis ('two-sided', 'greater', 'less').

    Returns:
        HypothesisTestResult containing statistics, p-value, CI, and decision.
    """
    arr = np.asarray(data, dtype=float)
    n = arr.size
    if n < 2:
        raise ValueError("At least 2 observations are required for a t-test.")
    if not (0 < alpha < 1):
        raise ValueError("Alpha must be strictly between 0 and 1.")
    if alternative not in ("two-sided", "greater", "less"):
        raise ValueError("Alternative must be 'two-sided', 'greater', or 'less'.")

    df = n - 1
    sample_mean = float(np.mean(arr))
    sample_std = float(np.std(arr, ddof=1))
    if sample_std == 0:
        raise ValueError("Sample variance is zero; cannot perform t-test.")

    sem = sample_std / math.sqrt(n)
    t_stat = (sample_mean - pop_mean) / sem

    if alternative == "two-sided":
        p_val = 2.0 * float(stats.t.sf(abs(t_stat), df=df))
        t_crit = float(stats.t.ppf(1.0 - alpha / 2.0, df=df))
        ci = (sample_mean - t_crit * sem, sample_mean + t_crit * sem)
    elif alternative == "greater":
        p_val = float(stats.t.sf(t_stat, df=df))
        t_crit = float(stats.t.ppf(1.0 - alpha, df=df))
        ci = (sample_mean - t_crit * sem, float("inf"))
    else:  # 'less'
        p_val = float(stats.t.cdf(t_stat, df=df))
        t_crit = float(stats.t.ppf(1.0 - alpha, df=df))
        ci = (float("-inf"), sample_mean + t_crit * sem)

    reject_null = bool(p_val < alpha)

    return HypothesisTestResult(
        statistic=t_stat,
        p_value=p_val,
        degrees_of_freedom=df,
        confidence_interval=ci,
        alpha=alpha,
        alternative=alternative,
        reject_null=reject_null
    )
