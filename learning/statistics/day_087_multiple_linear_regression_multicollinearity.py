import numpy as np
from typing import Dict, List, Tuple, Union, Optional
import scipy.stats as stats


class MultipleLinearRegression:
    """
    Ordinary Least Squares (OLS) Multiple Linear Regression model
    with detailed statistical metrics and diagnostics.
    """

    def __init__(self, fit_intercept: bool = True):
        self.fit_intercept = fit_intercept
        self.coefficients: Optional[np.ndarray] = None
        self.intercept: float = 0.0
        self.coef_std_err: Optional[np.ndarray] = None
        self.t_stats: Optional[np.ndarray] = None
        self.p_values: Optional[np.ndarray] = None
        self.r_squared: float = 0.0
        self.adj_r_squared: float = 0.0
        self.residual_variance: float = 0.0
        self._feature_names: List[str] = []

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        feature_names: Optional[List[str]] = None
    ) -> "MultipleLinearRegression":
        """
        Fit OLS regression model using normal equations with pseudo-inverse.
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).ravel()
        n_samples, n_features = X.shape

        if feature_names is None:
            self._feature_names = [f"x{i}" for i in range(n_features)]
        else:
            self._feature_names = list(feature_names)

        if self.fit_intercept:
            X_design = np.column_stack([np.ones(n_samples), X])
        else:
            X_design = X.copy()

        n_params = X_design.shape[1]
        df_deg = n_samples - n_params

        if df_deg <= 0:
            raise ValueError(
                f"Degrees of freedom must be > 0. Got n_samples={n_samples}, n_params={n_params}"
            )

        xtx = X_design.T @ X_design
        xtx_inv = np.linalg.pinv(xtx)
        beta = xtx_inv @ (X_design.T @ y)

        if self.fit_intercept:
            self.intercept = float(beta[0])
            self.coefficients = beta[1:]
        else:
            self.intercept = 0.0
            self.coefficients = beta

        predictions = X_design @ beta
        residuals = y - predictions
        rss = float(np.sum(residuals ** 2))
        tss = float(np.sum((y - np.mean(y)) ** 2))

        self.residual_variance = rss / df_deg
        cov_beta = self.residual_variance * xtx_inv
        std_errors = np.sqrt(np.maximum(0.0, np.diagonal(cov_beta)))

        self.t_stats = beta / np.where(std_errors == 0, 1e-12, std_errors)
        self.p_values = 2.0 * (1.0 - stats.t.cdf(np.abs(self.t_stats), df=df_deg))

        if self.fit_intercept:
            self.coef_std_err = std_errors[1:]
        else:
            self.coef_std_err = std_errors

        self.r_squared = 1.0 - (rss / tss) if tss > 0 else 0.0
        self.adj_r_squared = 1.0 - ((1.0 - self.r_squared) * (n_samples - 1) / df_deg)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict response for input samples.
        """
        if self.coefficients is None:
            raise RuntimeError("Model is not fitted yet.")
        X = np.asarray(X, dtype=np.float64)
        pred = X @ self.coefficients
        if self.fit_intercept:
            pred = pred + self.intercept
        return pred

    def summary(self) -> Dict[str, Union[float, Dict[str, Dict[str, float]]]]:
        """
        Return dictionary summary of fitted regression statistics.
        """
        if self.coefficients is None:
            raise RuntimeError("Model is not fitted yet.")

        coef_summary = {}
        for idx, name in enumerate(self._feature_names):
            coef_summary[name] = {
                "coefficient": float(self.coefficients[idx]),
                "std_err": float(self.coef_std_err[idx]),
                "t_stat": float(self.t_stats[idx + 1 if self.fit_intercept else idx]),
                "p_value": float(self.p_values[idx + 1 if self.fit_intercept else idx]),
            }

        return {
            "r_squared": float(self.r_squared),
            "adj_r_squared": float(self.adj_r_squared),
            "residual_variance": float(self.residual_variance),
            "intercept": float(self.intercept),
            "coefficients": coef_summary,
        }


def calculate_vif(X: np.ndarray) -> np.ndarray:
    """
    Calculate Variance Inflation Factor (VIF) for each column in feature matrix X.
    """
    X = np.asarray(X, dtype=np.float64)
    n_samples, n_features = X.shape
    vif = np.zeros(n_features)

    for i in range(n_features):
        y_i = X[:, i]
        X_i = np.delete(X, i, axis=1)

        X_design = np.column_stack([np.ones(n_samples), X_i])
        xtx_inv = np.linalg.pinv(X_design.T @ X_design)
        beta = xtx_inv @ (X_design.T @ y_i)
        pred = X_design @ beta
        residuals = y_i - pred
        rss = float(np.sum(residuals ** 2))
        tss = float(np.sum((y_i - np.mean(y_i)) ** 2))

        if tss == 0:
            vif[i] = 1.0
        else:
            r2 = max(0.0, 1.0 - (rss / tss))
            if r2 >= 1.0 - 1e-10:
                vif[i] = np.inf
            else:
                vif[i] = 1.0 / (1.0 - r2)

    return vif


def condition_number(X: np.ndarray) -> float:
    """
    Calculate condition number of feature matrix X.
    """
    X = np.asarray(X, dtype=np.float64)
    s = np.linalg.svd(X, compute_uv=False)
    if s[-1] == 0:
        return float("inf")
    return float(s[0] / s[-1])


def stepwise_vif_pruning(
    X: np.ndarray,
    threshold: float = 10.0,
    feature_names: Optional[List[str]] = None
) -> Tuple[np.ndarray, List[str], List[int]]:
    """
    Iteratively remove features with highest VIF above `threshold`.
    """
    X_curr = np.asarray(X, dtype=np.float64)
    n_features = X_curr.shape[1]

    if feature_names is None:
        names = [f"x{i}" for i in range(n_features)]
    else:
        names = list(feature_names)

    kept_indices = list(range(n_features))

    while len(kept_indices) > 1:
        vifs = calculate_vif(X_curr[:, kept_indices])
        max_vif_idx = int(np.argmax(vifs))
        max_vif = float(vifs[max_vif_idx])

        if max_vif > threshold:
            kept_indices.pop(max_vif_idx)
        else:
            break

    kept_names = [names[i] for i in kept_indices]
    X_pruned = X_curr[:, kept_indices]
    return X_pruned, kept_names, kept_indices
