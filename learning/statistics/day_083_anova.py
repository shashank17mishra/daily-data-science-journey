"""
Day 083: Analysis of Variance (ANOVA) Engine

This module provides a pure Python/NumPy implementation of One-Way Analysis of Variance
(ANOVA), Welch's ANOVA (for heteroscedastic data), ANOVA effect sizes (Eta-squared,
Omega-squared), assumption testing (Levene's test for variance homogeneity),
and pairwise post-hoc Tukey HSD test calculations.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Union
import numpy as np
from scipy import stats


@dataclass
class ANOVAResult:
    """Dataclass holding one-way ANOVA summary metrics."""
    ss_between: float
    ss_within: float
    ss_total: float
    df_between: int
    df_within: int
    df_total: int
    ms_between: float
    ms_within: float
    f_statistic: float
    p_value: float
    eta_squared: float
    omega_squared: float
    group_names: List[str]
    group_means: Dict[str, float]
    group_stds: Dict[str, float]


@dataclass
class AssumptionCheckResult:
    """Dataclass holding model assumption check results."""
    homogeneity_levene_stat: float
    homogeneity_p_value: float
    equal_variances_assumed: bool
    normality_p_values: Dict[str, float]


class OneWayANOVA:
    """
    Performs One-Way Analysis of Variance (ANOVA) with assumption diagnostics
    and robust effect size calculations.
    """

    def __init__(self, alpha: float = 0.05):
        """
        Initialize ANOVA Analyzer.

        Args:
            alpha: Significance level for statistical tests (default 0.05).
        """
        if not (0 < alpha < 1):
            raise ValueError("Alpha must be strictly between 0 and 1.")
        self.alpha = alpha

    def check_assumptions(
        self, data: Dict[str, Union[List[float], np.ndarray]]
    ) -> AssumptionCheckResult:
        """
        Check ANOVA assumptions: Normality (Shapiro-Wilk) and Homogeneity of Variances (Levene).

        Args:
            data: Dictionary mapping group names to numeric arrays.

        Returns:
            AssumptionCheckResult containing test statistics and p-values.
        """
        clean_data = {k: np.asarray(v, dtype=float) for k, v in data.items()}

        normality_p_values = {}
        for name, group in clean_data.items():
            if len(group) >= 3:
                _, p_val = stats.shapiro(group)
                normality_p_values[name] = float(p_val)
            else:
                normality_p_values[name] = float("nan")

        arrays = list(clean_data.values())
        levene_stat, levene_p = stats.levene(*arrays, center="median")

        return AssumptionCheckResult(
            homogeneity_levene_stat=float(levene_stat),
            homogeneity_p_value=float(levene_p),
            equal_variances_assumed=bool(levene_p > self.alpha),
            normality_p_values=normality_p_values
        )

    def fit(self, data: Dict[str, Union[List[float], np.ndarray]]) -> ANOVAResult:
        """
        Compute standard One-Way ANOVA table and effect sizes.

        Args:
            data: Dictionary mapping group names to array-like numeric samples.

        Returns:
            ANOVAResult dataclass instance.
        """
        if len(data) < 2:
            raise ValueError("ANOVA requires at least 2 comparison groups.")

        clean_data = {k: np.asarray(v, dtype=float) for k, v in data.items()}

        for name, arr in clean_data.items():
            if arr.ndim != 1 or len(arr) == 0:
                raise ValueError(f"Group '{name}' must be a non-empty 1D array.")

        k = len(clean_data)
        group_means = {group: float(np.mean(vals)) for group, vals in clean_data.items()}
        group_stds = {
            group: float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
            for group, vals in clean_data.items()
        }

        all_values = np.concatenate(list(clean_data.values()))
        grand_mean = float(np.mean(all_values))
        n_total = len(all_values)

        ss_total = float(np.sum((all_values - grand_mean) ** 2))

        ss_between = float(sum(
            len(arr) * ((np.mean(arr) - grand_mean) ** 2)
            for arr in clean_data.values()
        ))

        ss_within = float(sum(
            np.sum((arr - np.mean(arr)) ** 2)
            for arr in clean_data.values()
        ))

        df_between = k - 1
        df_within = n_total - k
        df_total = n_total - 1

        if df_within <= 0:
            raise ValueError("Insufficient degrees of freedom for error within groups.")

        ms_between = ss_between / df_between
        ms_within = ss_within / df_within

        f_stat = ms_between / ms_within if ms_within > 0 else 0.0
        p_val = float(stats.f.sf(f_stat, df_between, df_within))

        eta_sq = ss_between / ss_total if ss_total > 0 else 0.0

        omega_sq_denom = ss_total + ms_within
        if omega_sq_denom > 0:
            omega_sq = (ss_between - df_between * ms_within) / omega_sq_denom
            omega_sq = max(0.0, float(omega_sq))
        else:
            omega_sq = 0.0

        return ANOVAResult(
            ss_between=ss_between,
            ss_within=ss_within,
            ss_total=ss_total,
            df_between=df_between,
            df_within=df_within,
            df_total=df_total,
            ms_between=ms_between,
            ms_within=ms_within,
            f_statistic=f_stat,
            p_value=p_val,
            eta_squared=eta_sq,
            omega_squared=omega_sq,
            group_names=list(clean_data.keys()),
            group_means=group_means,
            group_stds=group_stds
        )

    def welch_anova(self, data: Dict[str, Union[List[float], np.ndarray]]) -> Tuple[float, float, float, float]:
        """
        Compute Welch's ANOVA for groups with unequal variances (heteroscedasticity).

        Args:
            data: Dictionary mapping group names to sample values.

        Returns:
            Tuple of (F_welch, df_between, df_error, p_value).
        """
        clean_data = {k: np.asarray(v, dtype=float) for k, v in data.items()}
        k = len(clean_data)
        if k < 2:
            raise ValueError("Welch's ANOVA requires at least 2 groups.")

        means = np.array([np.mean(arr) for arr in clean_data.values()])
        vars_ = np.array([np.var(arr, ddof=1) for arr in clean_data.values()])
        ns = np.array([len(arr) for arr in clean_data.values()])

        if np.any(vars_ <= 0):
            raise ValueError("All groups must have non-zero variance for Welch's ANOVA.")

        weights = ns / vars_
        w_total = np.sum(weights)

        x_bar_w = np.sum(weights * means) / w_total
        num = np.sum(weights * ((means - x_bar_w) ** 2)) / (k - 1)

        lambda_val = np.sum(((1.0 - (weights / w_total)) ** 2) / (ns - 1))
        denom = 1.0 + (2.0 * (k - 2) / (k ** 2 - 1)) * lambda_val

        f_welch = num / denom
        df1 = float(k - 1)
        df2 = float((k ** 2 - 1) / (3.0 * lambda_val))
        p_val = float(stats.f.sf(f_welch, df1, df2))

        return float(f_welch), df1, df2, p_val

    def tukey_hsd(
        self, data: Dict[str, Union[List[float], np.ndarray]]
    ) -> List[Dict[str, Union[str, float, bool]]]:
        """
        Compute pairwise Tukey's Honestly Significant Difference (HSD) post-hoc analysis.

        Args:
            data: Dictionary mapping group names to sample values.

        Returns:
            List of dictionary results for each group pair comparison.
        """
        result = self.fit(data)
        group_names = list(data.keys())
        clean_data = {k: np.asarray(v, dtype=float) for k, v in data.items()}

        pairwise_results = []
        ms_within = result.ms_within

        for i in range(len(group_names)):
            for j in range(i + 1, len(group_names)):
                g1, g2 = group_names[i], group_names[j]
                x1, x2 = clean_data[g1], clean_data[g2]
                n1, n2 = len(x1), len(x2)

                mean_diff = np.mean(x1) - np.mean(x2)
                se = np.sqrt(ms_within * 0.5 * (1.0 / n1 + 1.0 / n2))
                q_stat = abs(mean_diff) / se if se > 0 else 0.0
                p_val = float(stats.studentized_range.sf(q_stat, len(group_names), result.df_within))
                reject_null = p_val < self.alpha

                pairwise_results.append({
                    "group1": g1,
                    "group2": g2,
                    "mean_diff": float(mean_diff),
                    "q_stat": float(q_stat),
                    "p_val": float(p_val),
                    "reject_null": reject_null
                })

        return pairwise_results
