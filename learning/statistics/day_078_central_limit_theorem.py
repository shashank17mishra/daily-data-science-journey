import numpy as np
from typing import Dict, Any

class CLTExperiment:
    """
    Demonstrates the Central Limit Theorem using Monte Carlo sampling
    from a specified population distribution.
    """
    def __init__(self, population_generator, pop_mean: float, pop_std: float):
        """
        Initialize the CLT experiment with a population distribution.
        
        Args:
            population_generator: Callable that takes size=N and returns samples.
            pop_mean: Theoretical mean of the population.
            pop_std: Theoretical standard deviation of the population.
        """
        self.population_generator = population_generator
        self.pop_mean = pop_mean
        self.pop_std = pop_std

    def generate_sample_means(self, num_samples: int, sample_size: int) -> np.ndarray:
        """
        Generate multiple sample means from the population.
        
        Args:
            num_samples: Number of samples (experiments) to run.
            sample_size: Number of observations per sample (n).
            
        Returns:
            numpy.ndarray: Array of sample means.
        """
        # Shape: (num_samples, sample_size)
        samples = self.population_generator(size=(num_samples, sample_size))
        # Calculate mean along axis 1
        sample_means = np.mean(samples, axis=1)
        return sample_means

    def verify_clt(self, num_samples: int = 1000, sample_size: int = 30) -> Dict[str, Any]:
        """
        Verify properties predicted by the Central Limit Theorem.
        
        Args:
            num_samples: Number of sample means to generate.
            sample_size: Size of each individual sample.
            
        Returns:
            Dict containing empirical mean, theoretical mean, empirical std error,
            and theoretical standard error (pop_std / sqrt(sample_size)).
        """
        sample_means = self.generate_sample_means(num_samples, sample_size)
        
        empirical_mean = float(np.mean(sample_means))
        empirical_std = float(np.std(sample_means, ddof=1))
        
        theoretical_se = float(self.pop_std / np.sqrt(sample_size))
        
        return {
            "empirical_mean": empirical_mean,
            "theoretical_mean": self.pop_mean,
            "empirical_std_error": empirical_std,
            "theoretical_std_error": theoretical_se,
            "sample_means": sample_means
        }
