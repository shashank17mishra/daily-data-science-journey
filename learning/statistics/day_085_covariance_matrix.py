"""
Day 085: Covariance & Covariance Matrix
Comprehensive module implementing sample/population covariance, covariance matrix
computation from scratch, covariance-to-correlation matrix conversion, Mahalanobis distance,
and Covariance-based Principal Component Analysis (PCA).
"""

import numpy as np


def compute_covariance(x: np.ndarray, y: np.ndarray, ddof: int = 1) -> float:
    """
    Compute sample or population covariance between two 1D numeric vectors.

    Parameters:
        x (np.ndarray): 1D array of numeric values.
        y (np.ndarray): 1D array of numeric values.
        ddof (int): Delta Degrees of Freedom (1 for sample, 0 for population).

    Returns:
        float: Calculated covariance.

    Raises:
        ValueError: If inputs are not 1D, lengths mismatch, or N <= ddof.
    """
    x_arr = np.asarray(x, dtype=np.float64)
    y_arr = np.asarray(y, dtype=np.float64)

    if x_arr.ndim != 1 or y_arr.ndim != 1:
        raise ValueError("Inputs x and y must be 1D arrays.")
    if x_arr.shape[0] != y_arr.shape[0]:
        raise ValueError("Inputs x and y must have matching lengths.")
    n = x_arr.shape[0]
    if n <= ddof:
        raise ValueError(f"Number of samples ({n}) must be greater than ddof ({ddof}).")

    x_mean = np.mean(x_arr)
    y_mean = np.mean(y_arr)
    cov = np.sum((x_arr - x_mean) * (y_arr - y_mean)) / (n - ddof)
    return float(cov)


def compute_covariance_matrix(data: np.ndarray, ddof: int = 1) -> np.ndarray:
    """
    Compute covariance matrix for a 2D dataset of shape (N, D),
    where N is the number of samples and D is the number of features.

    Parameters:
        data (np.ndarray): 2D array of shape (N, D).
        ddof (int): Delta Degrees of Freedom.

    Returns:
        np.ndarray: Covariance matrix of shape (D, D).

    Raises:
        ValueError: If data is not 2D or sample count N <= ddof.
    """
    data_arr = np.asarray(data, dtype=np.float64)
    if data_arr.ndim != 2:
        raise ValueError("Input data must be a 2D array of shape (N_samples, D_features).")

    n, d = data_arr.shape
    if n <= ddof:
        raise ValueError(f"Number of samples ({n}) must be greater than ddof ({ddof}).")

    centered = data_arr - np.mean(data_arr, axis=0)
    cov_mat = (centered.T @ centered) / (n - ddof)
    return cov_mat


def covariance_to_correlation(cov_matrix: np.ndarray) -> np.ndarray:
    """
    Convert a symmetric covariance matrix into a Pearson correlation matrix.

    Parameters:
        cov_matrix (np.ndarray): Covariance matrix of shape (D, D).

    Returns:
        np.ndarray: Correlation matrix of shape (D, D).

    Raises:
        ValueError: If cov_matrix is non-square or diagonal contains non-positive values.
    """
    cov_arr = np.asarray(cov_matrix, dtype=np.float64)
    if cov_arr.ndim != 2 or cov_arr.shape[0] != cov_arr.shape[1]:
        raise ValueError("Input must be a square 2D matrix.")

    std_devs = np.sqrt(np.diag(cov_arr))
    if np.any(std_devs <= 0):
        raise ValueError("Diagonal entries (variances) must be strictly positive.")

    outer_std = np.outer(std_devs, std_devs)
    corr_mat = cov_arr / outer_std
    return np.clip(corr_mat, -1.0, 1.0)


def mahalanobis_distance(
    query_points: np.ndarray, reference_data: np.ndarray, regularize: float = 1e-6
) -> np.ndarray:
    """
    Compute Mahalanobis distance of query points relative to a reference distribution.

    Parameters:
        query_points (np.ndarray): Matrix of shape (M, D) or vector of shape (D,).
        reference_data (np.ndarray): Reference data matrix of shape (N, D).
        regularize (float): Regularization added to matrix diagonal for numerical stability.

    Returns:
        np.ndarray: Array of distances of shape (M,).
    """
    ref = np.asarray(reference_data, dtype=np.float64)
    queries = np.asarray(query_points, dtype=np.float64)

    if ref.ndim != 2:
        raise ValueError("Reference data must be a 2D array.")
    if queries.ndim == 1:
        queries = queries.reshape(1, -1)
    if ref.shape[1] != queries.shape[1]:
        raise ValueError("Dimension mismatch between query points and reference data.")

    mean_vec = np.mean(ref, axis=0)
    cov = compute_covariance_matrix(ref, ddof=1)
    cov_reg = cov + regularize * np.eye(cov.shape[0])
    inv_cov = np.linalg.inv(cov_reg)

    diff = queries - mean_vec
    distances = np.sqrt(np.sum((diff @ inv_cov) * diff, axis=1))
    return distances


def pca_via_covariance(data: np.ndarray, n_components: int = 2) -> dict:
    """
    Perform Principal Component Analysis (PCA) using eigen-decomposition of covariance matrix.

    Parameters:
        data (np.ndarray): Input matrix of shape (N, D).
        n_components (int): Number of principal components to extract.

    Returns:
        dict: Dictionary containing components, explained variance, ratio, and transformed data.
    """
    data_arr = np.asarray(data, dtype=np.float64)
    if data_arr.ndim != 2:
        raise ValueError("Input data must be a 2D array.")

    n_samples, n_features = data_arr.shape
    if n_components <= 0 or n_components > min(n_samples, n_features):
        raise ValueError("n_components must be positive and <= min(n_samples, n_features).")

    cov_mat = compute_covariance_matrix(data_arr, ddof=1)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_mat)

    idx = np.argsort(eigenvalues)[::-1]
    sorted_evals = np.maximum(eigenvalues[idx], 0.0)
    sorted_evecs = eigenvectors[:, idx]

    total_var = np.sum(sorted_evals)
    explained_variance = sorted_evals[:n_components]
    explained_variance_ratio = (
        explained_variance / total_var if total_var > 0 else np.zeros(n_components)
    )

    components = sorted_evecs[:, :n_components]
    centered_data = data_arr - np.mean(data_arr, axis=0)
    transformed = centered_data @ components

    return {
        "components": components,
        "explained_variance": explained_variance,
        "explained_variance_ratio": explained_variance_ratio,
        "transformed_data": transformed,
    }
