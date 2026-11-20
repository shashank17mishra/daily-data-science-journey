import numpy as np
from scipy import stats

class TwoSampleTTest:
    """Class for performing various two-sample t-tests and related statistics."""

    @staticmethod
    def welch_ttest(sample1, sample2, alpha=0.05):
        """
        Perform Welch's t-test for two independent samples with unequal variances.
        
        Args:
            sample1 (array-like): First sample measurements.
            sample2 (array-like): Second sample measurements.
            alpha (float): Significance level.
            
        Returns:
            dict: Dictionary containing t-statistic, p-value, degrees of freedom, confidence interval, and reject_null flag.
        """
        x1 = np.asarray(sample1, dtype=np.float64)
        x2 = np.asarray(sample2, dtype=np.float64)

        n1, n2 = len(x1), len(x2)
        mean1, mean2 = np.mean(x1), np.mean(x2)
        var1, var2 = np.var(x1, ddof=1), np.var(x2, ddof=1)

        se = np.sqrt((var1 / n1) + (var2 / n2))
        t_stat = (mean1 - mean2) / se

        # Welch-Satterthwaite degrees of freedom
        numerator = ((var1 / n1) + (var2 / n2)) ** 2
        denominator = ((var1 / n1) ** 2) / (n1 - 1) + ((var2 / n2) ** 2) / (n2 - 1)
        df = numerator / denominator

        p_val = 2 * (1 - stats.t.cdf(np.abs(t_stat), df))
        critical_t = stats.t.ppf(1 - alpha / 2, df)
        mean_diff = mean1 - mean2
        ci_lower = mean_diff - critical_t * se
        ci_upper = mean_diff + critical_t * se

        return {
            "t_statistic": float(t_stat),
            "p_value": float(p_val),
            "degrees_of_freedom": float(df),
            "confidence_interval": (float(ci_lower), float(ci_upper)),
            "reject_null": bool(p_val < alpha)
        }

    @staticmethod
    def student_ttest(sample1, sample2, alpha=0.05):
        """
        Perform Student's t-test assuming equal variances.
        
        Args:
            sample1 (array-like): First sample measurements.
            sample2 (array-like): Second sample measurements.
            alpha (float): Significance level.
            
        Returns:
            dict: Dictionary containing t-statistic, p-value, degrees of freedom, and reject_null flag.
        """
        x1 = np.asarray(sample1, dtype=np.float64)
        x2 = np.asarray(sample2, dtype=np.float64)

        n1, n2 = len(x1), len(x2)
        mean1, mean2 = np.mean(x1), np.mean(x2)
        var1, var2 = np.var(x1, ddof=1), np.var(x2, ddof=1)

        df = n1 + n2 - 2
        sp = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / df)
        se = sp * np.sqrt(1 / n1 + 1 / n2)
        
        t_stat = (mean1 - mean2) / se
        p_val = 2 * (1 - stats.t.cdf(np.abs(t_stat), df))

        return {
            "t_statistic": float(t_stat),
            "p_value": float(p_val),
            "degrees_of_freedom": int(df),
            "reject_null": bool(p_val < alpha)
        }

    @staticmethod
    def paired_ttest(sample1, sample2, alpha=0.05):
        """
        Perform a paired samples t-test.
        
        Args:
            sample1 (array-like): Initial measurements.
            sample2 (array-like): Follow-up measurements.
            alpha (float): Significance level.
            
        Returns:
            dict: Dictionary containing t-statistic, p-value, degrees of freedom, and reject_null flag.
        """
        x1 = np.asarray(sample1, dtype=np.float64)
        x2 = np.asarray(sample2, dtype=np.float64)

        if len(x1) != len(x2):
            raise ValueError("Paired samples must have the same number of observations.")

        differences = x1 - x2
        n = len(differences)
        mean_diff = np.mean(differences)
        var_diff = np.var(differences, ddof=1)
        se = np.sqrt(var_diff / n)

        t_stat = mean_diff / se
        df = n - 1
        p_val = 2 * (1 - stats.t.cdf(np.abs(t_stat), df))

        return {
            "t_statistic": float(t_stat),
            "p_value": float(p_val),
            "degrees_of_freedom": int(df),
            "reject_null": bool(p_val < alpha)
        }
