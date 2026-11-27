import numpy as np


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Numerically stable sigmoid activation function.

    Maps real-valued inputs (log-odds) to probabilities in range (0, 1).
    Uses piecewise calculation to avoid overflow for extreme negative inputs.
    """
    z_arr = np.asarray(z, dtype=np.float64)
    return np.where(
        z_arr >= 0,
        1.0 / (1.0 + np.exp(-z_arr)),
        np.exp(z_arr) / (1.0 + np.exp(z_arr))
    )


def logit(p: np.ndarray, eps: float = 1e-15) -> np.ndarray:
    """Computes the logit (log-odds) function for given probabilities.

    logit(p) = log(p / (1 - p))
    Clips probabilities to [eps, 1 - eps] to ensure numerical stability.
    """
    p_arr = np.clip(np.asarray(p, dtype=np.float64), eps, 1.0 - eps)
    return np.log(p_arr / (1.0 - p_arr))


class LogisticRegressionLogOdds:
    """Binary Logistic Regression implementing explicit log-odds transformations.

    Models probability P(Y=1|X) = sigmoid(X @ w + b).
    Provides explicit utilities for predicting log-odds, calculating odds ratios,
    and performing batch gradient descent on binary cross-entropy loss.
    """

    def __init__(self, learning_rate: float = 0.1, max_iter: int = 1000, tol: float = 1e-6):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.tol = tol
        self.weights = None
        self.bias = 0.0
        self.loss_history = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LogisticRegressionLogOdds":
        """Fits the logistic regression model parameters using gradient descent.

        Args:
            X: Input feature matrix of shape (n_samples, n_features).
            y: Target binary labels (0 or 1) of shape (n_samples,).

        Returns:
            self
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        n_samples, n_features = X.shape

        self.weights = np.zeros(n_features, dtype=np.float64)
        self.bias = 0.0
        self.loss_history = []

        for iteration in range(self.max_iter):
            log_odds = self.predict_log_odds(X)
            y_pred = sigmoid(log_odds)

            # Compute Binary Cross-Entropy Loss
            loss = -np.mean(
                y * np.log(np.clip(y_pred, 1e-15, 1.0))
                + (1.0 - y) * np.log(np.clip(1.0 - y_pred, 1e-15, 1.0))
            )
            self.loss_history.append(loss)

            # Calculate gradients wrt weights and bias
            dw = (1.0 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (1.0 / n_samples) * np.sum(y_pred - y)

            # Update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

            # Early stopping check based on loss convergence
            if iteration > 0 and abs(self.loss_history[-2] - self.loss_history[-1]) < self.tol:
                break

        return self

    def predict_log_odds(self, X: np.ndarray) -> np.ndarray:
        """Calculates raw model output z = X @ weights + bias (log-odds)."""
        if self.weights is None:
            raise ValueError("Model must be fitted before calling predict_log_odds.")
        X = np.asarray(X, dtype=np.float64)
        return np.dot(X, self.weights) + self.bias

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predicts binary class probability P(Y=1|X) using the sigmoid function."""
        log_odds = self.predict_log_odds(X)
        return sigmoid(log_odds)

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """Predicts discrete binary labels (0 or 1) based on a probability threshold."""
        return (self.predict_proba(X) >= threshold).astype(int)

    def odds_ratios(self) -> np.ndarray:
        """Calculates the feature odds ratios exp(weights).

        An odds ratio > 1 indicates that an increase in feature value increases the odds of Y=1.
        """
        if self.weights is None:
            raise ValueError("Model must be fitted before computing odds ratios.")
        return np.exp(self.weights)
