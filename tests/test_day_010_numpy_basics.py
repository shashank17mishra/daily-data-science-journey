import numpy as np
import pytest
from learning.numpy.day_010_numpy_basics import compute_matrix_stats, normalize_matrix

def test_compute_matrix_stats():
    arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=float)
    stats = compute_matrix_stats(arr)
    assert stats["shape"] == (2, 3)
    assert stats["mean"] == 3.5
    assert stats["row_sums"] == [6.0, 15.0]
    assert stats["col_sums"] == [5.0, 7.0, 9.0]

def test_normalize_matrix():
    arr = np.array([[10, 20], [30, 40]], dtype=float)
    norm = normalize_matrix(arr)
    assert norm[0, 0] == 0.0
    assert norm[1, 1] == 1.0
    assert norm[0, 1] == pytest.approx(0.333333, abs=1e-4)
