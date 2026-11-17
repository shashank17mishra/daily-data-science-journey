import numpy as np
import pytest
from learning.statistics.day_078_central_limit_theorem import CLTExperiment

def test_clt_exponential_distribution():
    """
    Test CLT using an Exponential distribution (highly skewed).
    For Exponential(lambda), Mean = 1/lambda, Std = 1/lambda.
    Let lambda = 2.0, so Mean = 0.5, Std = 0.5.
    """
    lam = 2.0
    pop_mean = 1.0 / lam
    pop_std = 1.0 / lam
    
    # Population generator using numpy exponential
    pop_gen = lambda size: np.random.exponential(scale=1.0/lam, size=size)
    
    experiment = CLTExperiment(pop_gen, pop_mean, pop_std)
    
    num_samples = 2000
    sample_size = 50
    results = experiment.verify_clt(num_samples=num_samples, sample_size=sample_size)
    
    # 1. Mean of sample means should be very close to population mean
    assert np.isclose(results["empirical_mean"], results["theoretical_mean"], atol=0.05)
    
    # 2. Standard error of sample means should be close to theoretical SE (pop_std / sqrt(n))
    assert np.isclose(results["empirical_std_error"], results["theoretical_std_error"], rtol=0.15)
    
    # 3. Distribution of sample means should approach normality (checked via simple bounds or skewness/kurtosis proxy)
    sample_means = results["sample_means"]
    # For a normal distribution, roughly 95% of data falls within +/- 2 standard errors
    z_scores = (sample_means - results["theoretical_mean"]) / results["empirical_std_error"]
    within_2_se = np.mean(np.abs(z_scores) <= 2.0)
    
    # Expect roughly 95% (+/- 3% tolerance for stochastic variation)
    assert 0.92 <= within_2_se <= 0.98

def test_clt_uniform_distribution():
    """
    Test CLT using a Continuous Uniform distribution [0, 1].
    Mean = 0.5, Std = sqrt(1/12) ≈ 0.2887.
    """
    low, high = 0.0, 1.0
    pop_mean = (low + high) / 2.0
    pop_std = np.sqrt((high - low)**2 / 12.0)
    
    pop_gen = lambda size: np.random.uniform(low, high, size=size)
    
    experiment = CLTExperiment(pop_gen, pop_mean, pop_std)
    
    results = experiment.verify_clt(num_samples=1500, sample_size=30)
    
    assert np.isclose(results["empirical_mean"], results["theoretical_mean"], atol=0.03)
    assert np.isclose(results["empirical_std_error"], results["theoretical_std_error"], rtol=0.15)
