"""
Day 086: Simple Linear Regression Theory & Practical OLS Implementation

This module provides a complete, mathematically rigorous implementation of Simple
Linear Regression using Ordinary Least Squares (OLS) from first principles.
Includes hypothesis testing, standard errors, ANOVA breakdown, confidence intervals,
and prediction intervals.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Union
import numpy as np
from scipy import stats


@dataclass
class RegressionSummary:
    """Dataclass holding complete theoretical statistics for simple linear regression."""
    beta_0: float
    beta_1: float
    se_beta_0: float
    se_beta_1: float
    t_stat_beta_0: float
    t_stat_beta_1: float
    p_val_beta_0: float
    p_val_beta_1: float
    r_squared: float
    adj_r_squared: float
    residual_std_error: float
    f_statistic: float
    f_p_value: float
    n_samples: int
    df_residual: int


class SimpleLinearRegression:
    """
    Ordinary Least Squares (OLS) Simple Linear Regression model.

    Theoretical Formulas Implemented:
        beta_1 = S_xy / S_xx
        beta_0 = y_bar - beta_1 * x_bar
        S_xx = sum((x - x_bar)^2)
        S_yy = sum((y - y_bar)^2)
        S_xy = sum((x - x_bar)*(y - y_bar))
        MSE = SSE / (n - 2)
        SE(beta_1) = sqrt(MSE / S_xx)
        SE(beta_0) = sqrt(MSE * (1/n + x_bar^2 / S_xx))
    """

    def __init__(self) -> None:
        self.fitted: bool = False
        self.beta_0: float = 0.0
        self.beta_1: float = 0.0
        self.x_mean: float = 0.0
        self.y_mean: float = 0.0
        self.s_xx: float = 0.0
        self.s_yy: float = 0.0
        self.s_xy: float = 0.0
        self.sse: float = 0.0
        self.ssr: float = 0.0
        self.sst: float = 0.0
        self.mse: float = 0.0
        self.n: int = 0
        self.df_res: int = 0
        self.se_beta_0: float = 0.0
        self.se_beta_1: float = 0.0

    def fit(self, x: Union[List[float], np.ndarray], y: Union[List[float], np.ndarray]) -> "SimpleLinearRegression":
        """Fits the linear model y = beta_0 + beta_1 * x using Ordinary Least Squares."""
        x_arr = np.asarray(x, dtype=np.float64).flatten()
        y_arr = np.asarray(y, dtype=np.float64).flatten()

        if len(x_arr) != len(y_arr):
            raise ValueError("Input arrays x and y must have the same length.")
        if len(x_arr) < 3:
            raise ValueError("At least 3 data points are required for regression inference.")

        self.n = len(x_arr)
        self.df_res = self.n - 2

        self.x_mean = float(np.mean(x_arr))
        self.y_mean = float(np.mean(y_arr))

        dx = x_arr - self.x_mean
        dy = y_arr - self.y_mean

        self.s_xx = float(np.sum(dx ** 2))
        self.s_yy = float(np.sum(dy ** 2))
        self.s_xy = float(np.sum(dx * dy))

        if self.s_xx == 0:
            raise ValueError("Variance of x is zero; cannot compute linear regression slope.")

        self.beta_1 = self.s_xy / self.s_xx
        self.beta_0 = self.y_mean - self.beta_1 * self.x_mean

        y_pred = self.beta_0 + self.beta_1 * x_arr
        residuals = y_arr - y_pred

        self.sse = max(0.0, float(np.sum(residuals ** 2)))
        self.sst = float(self.s_yy)
        self.ssr = self.sst - self.sse

        self.mse = self.sse / self.df_res if self.df_res > 0 else 0.0

        if self.mse > 1e-14:
            self.se_beta_1 = float(np.sqrt(self.mse / self.s_xx))
            self.se_beta_0 = float(np.sqrt(self.mse * (1.0 / self.n + (self.x_mean ** 2) / self.s_xx)))
        else:
            self.se_beta_1 = 0.0
            self.se_beta_0 = 0.0

        self.fitted = True
        return self

    def predict(self, x: Union[float, List[float], np.ndarray]) -> np.ndarray:
        """Predicts response variable for given feature values."""
        if not self.fitted:
            raise RuntimeError("Model must be fitted before making predictions.")
        x_arr = np.asarray(x, dtype=np.float64)
        return self.beta_0 + self.beta_1 * x_arr

    def summary(self) -> RegressionSummary:
        """Computes and returns detailed statistical inference summary of the regression model."""
        if not self.fitted:
            raise RuntimeError("Model must be fitted before obtaining summary.")

        t_stat_0 = self.beta_0 / self.se_beta_0 if self.se_beta_0 > 0 else float("inf")
        t_stat_1 = self.beta_1 / self.se_beta_1 if self.se_beta_1 > 0 else float("inf")

        if np.isinf(t_stat_0):
            p_val_0 = 0.0
        else:
            p_val_0 = float(2.0 * (1.0 - stats.t.cdf(abs(t_stat_0), df=self.df_res)))

        if np.isinf(t_stat_1):
            p_val_1 = 0.0
        else:
            p_val_1 = float(2.0 * (1.0 - stats.t.cdf(abs(t_stat_1), df=self.df_res)))

        r_squared = float(self.ssr / self.sst) if self.sst > 0 else 1.0
        r_squared = max(0.0, min(1.0, r_squared))
        adj_r_squared = float(1.0 - (1.0 - r_squared) * (self.n - 1) / self.df_res)

        if self.mse > 0:
            f_stat = float((self.ssr / 1.0) / self.mse)
            f_p_val = float(1.0 - stats.f.cdf(f_stat, dfn=1, dfd=self.df_res))
        else:
            f_stat = float("inf")
            f_p_val = 0.0

        return RegressionSummary(
            beta_0=self.beta_0,
            beta_1=self.beta_1,
            se_beta_0=self.se_beta_0,
            se_beta_1=self.se_beta_1,
            t_stat_beta_0=t_stat_0,
            t_stat_beta_1=t_stat_1,
            p_val_beta_0=p_val_0,
            p_val_beta_1=p_val_1,
            r_squared=r_squared,
            adj_r_squared=adj_r_squared,
            residual_std_error=float(np.sqrt(self.mse)),
            f_statistic=f_stat,
            f_p_value=f_p_val,
            n_samples=self.n,
            df_residual=self.df_res,
        )

    def confidence_interval(self, alpha: float = 0.05) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Calculates (1 - alpha) confidence intervals for (beta_0, beta_1)."""
        if not self.fitted:
            raise RuntimeError("Model must be fitted to compute confidence intervals.")
        if not (0.0 < alpha < 1.0):
            raise ValueError("Alpha must be between 0 and 1.")

        t_crit = float(stats.t.ppf(1.0 - alpha / 2.0, df=self.df_res))

        ci_b0 = (self.beta_0 - t_crit * self.se_beta_0, self.beta_0 + t_crit * self.se_beta_0)
        ci_b1 = (self.beta_1 - t_crit * self.se_beta_1, self.beta_1 + t_crit * self.se_beta_1)

        return ci_b0, ci_b1

    def predict_interval(
        self, x_new: Union[float, List[float], np.ndarray], alpha: float = 0.05
    ) -> Dict[str, np.ndarray]:
        """
        Calculates confidence interval for mean response E[Y|X] and prediction interval
        for individual new observation Y_new at x_new.
        """
        if not self.fitted:
            raise RuntimeError("Model must be fitted before predicting intervals.")
        if not (0.0 < alpha < 1.0):
            raise ValueError("Alpha must be between 0 and 1.")

        x_arr = np.asarray(x_new, dtype=np.float64)
        y_pred = self.predict(x_arr)
        t_crit = float(stats.t.ppf(1.0 - alpha / 2.0, df=self.df_res))

        se_mean = np.sqrt(self.mse * (1.0 / self.n + ((x_arr - self.x_mean) ** 2) / self.s_xx))
        se_pred = np.sqrt(self.mse * (1.0 + 1.0 / self.n + ((x_arr - self.x_mean) ** 2) / self.s_xx))

        return {
            "prediction": y_pred,
            "ci_lower": y_pred - t_crit * se_mean,
            "ci_upper": y_pred + t_crit * se_mean,
            "pi_lower": y_pred - t_crit * se_pred,
            "pi_upper": y_pred + t_crit * se_pred,
        }
