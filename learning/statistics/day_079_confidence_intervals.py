import math
from typing import Callable, Tuple, Union, Optional
import numpy as np
from scipy import stats


def mean_confidence_interval(
    data: Union[list, np.ndarray],
    confidence: float = 0.95,
    known_std: Optional[float] = None
) -> Tuple[float, float]:
    """
    Calculate confidence interval for sample mean.

    Parameters:
    -----------
    data : array-like
        Sample observations.
    confidence : float
        Confidence level (0 < confidence < 1), e.g., 0.95 for 95% CI.
    known_std : float, optional
        Population standard deviation if known (uses Z-distribution).
        If None, sample standard deviation is used (uses Student's t-distribution).

    Returns:
    --------
    Tuple[float, float] : (lower_bound, upper_bound)
    """
    arr = np.asarray(data, dtype=float)
    if arr.size < 1:
        raise ValueError("Data array cannot be empty.")
    if arr.size < 2 and known_std is None:
        raise ValueError("At least 2 data points required when population standard deviation is unknown.")
    if not (0.0 < confidence < 1.0):
        raise ValueError("Confidence level must be strictly between 0 and 1.")

    n = arr.size
    mean = float(np.mean(arr))
    alpha = 1.0 - confidence

    if known_std is not None:
        if known_std <= 0:
            raise ValueError("known_std must be positive.")
        z_score = stats.norm.ppf(1.0 - alpha / 2.0)
        margin_of_error = z_score * (known_std / math.sqrt(n))
    else:
        sample_std = float(np.std(arr, ddof=1))
        t_score = stats.t.ppf(1.0 - alpha / 2.0, df=n - 1)
        margin_of_error = t_score * (sample_std / math.sqrt(n))

    return (mean - margin_of_error, mean + margin_of_error)


def proportion_confidence_interval(
    successes: int,
    n: int,
    confidence: float = 0.95,
    method: str = "wilson"
) -> Tuple[float, float]:
    """
    Calculate confidence interval for a binomial proportion.

    Parameters:
    -----------
    successes : int
        Number of successes.
    n : int
        Total sample size.
    confidence : float
        Confidence level (0 < confidence < 1).
    method : str
        Method to use: 'wilson' or 'wald'.

    Returns:
    --------
    Tuple[float, float] : (lower_bound, upper_bound)
    """
    if n <= 0:
        raise ValueError("Sample size n must be positive.")
    if not (0 <= successes <= n):
        raise ValueError("Successes must be an integer between 0 and n.")
    if not (0.0 < confidence < 1.0):
        raise ValueError("Confidence level must be strictly between 0 and 1.")

    p_hat = successes / n
    alpha = 1.0 - confidence
    z = stats.norm.ppf(1.0 - alpha / 2.0)

    if method == "wald":
        se = math.sqrt((p_hat * (1.0 - p_hat)) / n)
        lower = max(0.0, p_hat - z * se)
        upper = min(1.0, p_hat + z * se)
    elif method == "wilson":
        denominator = 1.0 + (z ** 2) / n
        center = (p_hat + (z ** 2) / (2.0 * n)) / denominator
        spread = (z / denominator) * math.sqrt(
            (p_hat * (1.0 - p_hat)) / n + (z ** 2) / (4.0 * (n ** 2))
        )
        lower = max(0.0, center - spread)
        upper = min(1.0, center + spread)
    else:
        raise ValueError("Method must be either 'wilson' or 'wald'.")

    return (float(lower), float(upper))


def difference_of_means_ci(
    sample1: Union[list, np.ndarray],
    sample2: Union[list, np.ndarray],
    confidence: float = 0.95,
    equal_var: bool = False
) -> Tuple[float, float]:
    """
    Calculate confidence interval for the difference between two sample means (mean1 - mean2).

    Parameters:
    -----------
    sample1, sample2 : array-like
        Independent samples.
    confidence : float
        Confidence level (0 < confidence < 1).
    equal_var : bool
        If True, assume equal population variances (pooled t-interval).
        If False, use Welch's t-interval (unpooled).

    Returns:
    --------
    Tuple[float, float] : (lower_bound, upper_bound)
    """
    s1 = np.asarray(sample1, dtype=float)
    s2 = np.asarray(sample2, dtype=float)

    if s1.size < 2 or s2.size < 2:
        raise ValueError("Both samples must contain at least 2 data points.")
    if not (0.0 < confidence < 1.0):
        raise ValueError("Confidence level must be strictly between 0 and 1.")

    n1, n2 = s1.size, s2.size
    mean1, mean2 = float(np.mean(s1)), float(np.mean(s2))
    diff = mean1 - mean2
    var1, var2 = float(np.var(s1, ddof=1)), float(np.var(s2, ddof=1))
    alpha = 1.0 - confidence

    if equal_var:
        df = n1 + n2 - 2
        pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / df
        se = math.sqrt(pooled_var * (1.0 / n1 + 1.0 / n2))
    else:
        v1, v2 = var1 / n1, var2 / n2
        se = math.sqrt(v1 + v2)
        if se == 0:
            return (diff, diff)
        df = ((v1 + v2) ** 2) / ((v1 ** 2) / (n1 - 1) + (v2 ** 2) / (n2 - 1))

    t_score = stats.t.ppf(1.0 - alpha / 2.0, df=df)
    margin_of_error = t_score * se

    return (diff - margin_of_error, diff + margin_of_error)


def bootstrap_ci(
    data: Union[list, np.ndarray],
    stat_fn: Callable[[np.ndarray], float] = np.mean,
    confidence: float = 0.95,
    n_resamples: int = 2000,
    random_state: Optional[int] = None
) -> Tuple[float, float]:
    """
    Calculate non-parametric bootstrap percentile confidence interval.

    Parameters:
    -----------
    data : array-like
        Sample data.
    stat_fn : callable
        Function that accepts 1D array and returns a scalar statistic.
    confidence : float
        Confidence level (0 < confidence < 1).
    n_resamples : int
        Number of bootstrap samples to draw.
    random_state : int, optional
        Seed for reproducible random sampling.

    Returns:
    --------
    Tuple[float, float] : (lower_bound, upper_bound)
    """
    arr = np.asarray(data, dtype=float)
    if arr.size == 0:
        raise ValueError("Data array cannot be empty.")
    if not (0.0 < confidence < 1.0):
        raise ValueError("Confidence level must be strictly between 0 and 1.")
    if n_resamples <= 0:
        raise ValueError("n_resamples must be positive.")

    rng = np.random.default_rng(random_state)
    n = arr.size
    bootstrap_stats = np.empty(n_resamples, dtype=float)

    for i in range(n_resamples):
        sample = rng.choice(arr, size=n, replace=True)
        bootstrap_stats[i] = float(stat_fn(sample))

    alpha = 1.0 - confidence
    lower_pct = (alpha / 2.0) * 100.0
    upper_pct = (1.0 - alpha / 2.0) * 100.0

    lower = float(np.percentile(bootstrap_stats, lower_pct))
    upper = float(np.percentile(bootstrap_stats, upper_pct))

    return (lower, upper)
