"""
Chi-Square Test of Independence for Categorical Variables.

This module provides a class `ChiSquareTest` to perform contingency table analysis,
calculating expected frequencies, chi-square test statistic, p-value, degrees of freedom,
Cramer's V effect size, standardized residuals, and checking assumption validity.
"""

from typing import Dict, Any
import numpy as np
from scipy.stats import chi2


class ChiSquareTest:
    """Performs Chi-Square Test of Independence on a 2D contingency table."""

    def __init__(self, observed: np.ndarray) -> None:
        """
        Initialize with observed categorical contingency matrix.

        :param observed: 2D array-like of observed non-negative counts.
        """
        self.observed = np.asarray(observed, dtype=np.float64)
        if self.observed.ndim != 2:
            raise ValueError("Observed matrix must be 2-dimensional.")
        if np.any(self.observed < 0):
            raise ValueError("Observed counts must be non-negative.")
        if self.observed.shape[0] < 2 or self.observed.shape[1] < 2:
            raise ValueError("Contingency table must be at least 2x2.")
        if np.sum(self.observed) == 0:
            raise ValueError("Observed table cannot be entirely zero.")

    def compute_expected(self) -> np.ndarray:
        """Compute expected frequencies under the independence null hypothesis."""
        row_sums = self.observed.sum(axis=1, keepdims=True)
        col_sums = self.observed.sum(axis=0, keepdims=True)
        total = self.observed.sum()
        return (row_sums @ col_sums) / total

    def check_assumptions(self) -> Dict[str, Any]:
        """
        Check Chi-Square test assumptions according to Cochran's rules:
        1. All expected cell counts are >= 1.
        2. No more than 20% of expected cell counts are < 5.
        """
        expected = self.compute_expected()
        total_cells = expected.size
        count_less_than_5 = np.sum(expected < 5.0)
        pct_less_than_5 = (count_less_than_5 / total_cells) * 100.0
        min_expected = np.min(expected)

        valid = bool((min_expected >= 1.0) and (pct_less_than_5 <= 20.0))

        return {
            "valid": valid,
            "min_expected": float(min_expected),
            "pct_expected_below_5": float(pct_less_than_5),
            "cells_below_5": int(count_less_than_5),
            "total_cells": int(total_cells),
        }

    def analyze(self, correction: bool = True) -> Dict[str, Any]:
        """
        Perform the Chi-Square test of independence.

        :param correction: Apply Yates' continuity correction for 2x2 tables if True.
        :return: Dictionary containing test statistics, p-value, df, effect size, etc.
        """
        expected = self.compute_expected()
        r, c = self.observed.shape
        df = (r - 1) * (c - 1)
        total = float(self.observed.sum())

        diff = np.abs(self.observed - expected)
        if correction and r == 2 and c == 2:
            diff = np.maximum(0.0, diff - 0.5)

        chi2_stat = np.sum((diff ** 2) / expected)
        p_val = chi2.sf(chi2_stat, df)

        min_dim = min(r - 1, c - 1)
        cramers_v = np.sqrt(chi2_stat / (total * min_dim)) if min_dim > 0 else 0.0

        row_prop = self.observed.sum(axis=1, keepdims=True) / total
        col_prop = self.observed.sum(axis=0, keepdims=True) / total
        variance = expected * (1.0 - row_prop) * (1.0 - col_prop)

        with np.errstate(divide="ignore", invalid="ignore"):
            std_residuals = np.where(variance > 0, (self.observed - expected) / np.sqrt(variance), 0.0)

        assumptions = self.check_assumptions()

        return {
            "chi2_stat": float(chi2_stat),
            "p_value": float(p_val),
            "degrees_of_freedom": int(df),
            "cramers_v": float(cramers_v),
            "observed": self.observed.tolist(),
            "expected": expected.tolist(),
            "standardized_residuals": std_residuals.tolist(),
            "assumptions_met": assumptions["valid"],
            "assumption_details": assumptions,
        }
