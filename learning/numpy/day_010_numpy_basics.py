"""
Day 010: NumPy Array Operations, Indexing, and Vectorized Aggregations.
"""
import numpy as np

def compute_matrix_stats(matrix: np.ndarray) -> dict:
    """Computes basic statistical properties of a NumPy 2D array."""
    if not isinstance(matrix, np.ndarray) or matrix.ndim != 2:
        raise ValueError("Input must be a 2D NumPy array.")

    return {
        "shape": matrix.shape,
        "mean": float(np.mean(matrix)),
        "std": float(np.std(matrix)),
        "row_sums": np.sum(matrix, axis=1).tolist(),
        "col_sums": np.sum(matrix, axis=0).tolist()
    }

def normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    """Applies Min-Max normalization to scale values between 0.0 and 1.0."""
    min_val = np.min(matrix)
    max_val = np.max(matrix)
    if min_val == max_val:
        return np.zeros_like(matrix, dtype=float)
    return (matrix - min_val) / (max_val - min_val)
