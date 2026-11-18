import pytest
import numpy as np
from scipy import stats

from learning.statistics.day_079_confidence_intervals import (
    mean_confidence_interval,
    proportion_confidence_interval,
    difference_of_means_ci,
    bootstrap_ci,
)


def test_mean_confidence_interval_t_distribution():
    data = [10.2, 11.5, 9.8, 12.1, 10.5, 11.0, 10.8]
    lower, upper = mean_confidence_interval(data, confidence=0.95)
    
    # Reference calculated via scipy.stats
    expected_lower, expected_upper = stats.t.interval(
        0.95, df=len(data) - 1, loc=np.mean(data), scale=stats.sem(data)
    )
    
    assert pytest.approx(lower, rel=1e-5) == expected_lower
    assert pytest.approx(upper, rel=1e-5) == expected_upper
    assert lower < np.mean(data) < upper


def test_mean_confidence_interval_z_distribution():
    data = [100, 104, 98, 102, 96, 105]
    sigma = 3.5
    lower, upper = mean_confidence_interval(data, confidence=0.90, known_std=sigma)
    
    expected_lower, expected_upper = stats.norm.interval(
        0.90, loc=np.mean(data), scale=sigma / np.sqrt(len(data))
    )
    
    assert pytest.approx(lower, rel=1e-5) == expected_lower
    assert pytest.approx(upper, rel=1e-5) == expected_upper


def test_proportion_confidence_interval_wald_and_wilson():
    successes = 45
    n = 100
    
    lower_wald, upper_wald = proportion_confidence_interval(successes, n, method="wald")
    lower_wilson, upper_wilson = proportion_confidence_interval(successes, n, method="wilson")
    
    assert 0.0 <= lower_wald < 0.45 < upper_wald <= 1.0
    assert 0.0 <= lower_wilson < 0.45 < upper_wilson <= 1.0
    
    # Wilson should be slightly tighter or shifted compared to naive Wald
    assert lower_wilson != lower_wald


def test_difference_of_means_ci_welch_and_pooled():
    group_a = [24, 28, 30, 22, 27, 32]
    group_b = [18, 20, 15, 22, 19, 17]
    
    lower_welch, upper_welch = difference_of_means_ci(group_a, group_b, confidence=0.95, equal_var=False)
    lower_pooled, upper_pooled = difference_of_means_ci(group_a, group_b, confidence=0.95, equal_var=True)
    
    diff = np.mean(group_a) - np.mean(group_b)
    assert lower_welch < diff < upper_welch
    assert lower_pooled < diff < upper_pooled


def test_bootstrap_ci_reproducibility_and_stat():
    np.random.seed(42)
    data = np.random.normal(loc=50.0, scale=10.0, size=50)
    
    lower1, upper1 = bootstrap_ci(data, stat_fn=np.median, confidence=0.95, n_resamples=1000, random_state=123)
    lower2, upper2 = bootstrap_ci(data, stat_fn=np.median, confidence=0.95, n_resamples=1000, random_state=123)
    
    assert lower1 == lower2
    assert upper1 == upper2
    assert lower1 < np.median(data) < upper1


def test_input_validation_errors():
    with pytest.raises(ValueError, match="At least 2 data points required"):
        mean_confidence_interval([5.0], confidence=0.95)
        
    with pytest.raises(ValueError, match="Confidence level must be strictly between 0 and 1"):
        proportion_confidence_interval(10, 20, confidence=1.5)
        
    with pytest.raises(ValueError, match="Method must be either 'wilson' or 'wald'"):
        proportion_confidence_interval(10, 20, method="unknown")
        
    with pytest.raises(ValueError, match="Both samples must contain at least 2 data points"):
        difference_of_means_ci([1.0], [2.0, 3.0])
