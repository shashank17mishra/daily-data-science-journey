"""
Unit tests for Day 085: Covariance & Covariance Matrix
"""

import numpy as np
import pytest

from learning.statistics.day_085_covariance_matrix import (
    compute_covariance,
    compute_covariance_matrix,
    covariance_to_correlation,
    mahalanobis_distance,
    pca_via_covariance,
)


def test_compute_covariance_matches_numpy():
    np.random.seed(42)
    x = np.random.randn(50)
    y = 2.0 * x + np.random.randn(50) * 0.5

    sample_cov = compute_covariance(x, y, ddof=1)
    expected_sample = np.cov(x, y, ddof=1)[0, 1]
    np.testing.assert_allclose(sample_cov, expected_sample, rtol=1e-6)

    pop_cov = compute_covariance(x, y, ddof=0)
    expected_pop = np.cov(x, y, ddof=0)[0, 1]
    np.testing.assert_allclose(pop_cov, expected_pop, rtol=1e-6)


def test_compute_covariance_matrix_matches_numpy():
    np.random.seed(42)
    data = np.random.randn(100, 4)

    cov_mat = compute_covariance_matrix(data, ddof=1)
    expected_cov = np.cov(data, rowvar=False, ddof=1)
    np.testing.assert_allclose(cov_mat, expected_cov, rtol=1e-6)


def test_covariance_to_correlation():
    np.random.seed(42)
    data = np.random.randn(80, 3)
    cov_mat = compute_covariance_matrix(data)
    corr_mat = covariance_to_correlation(cov_mat)

    expected_corr = np.corrcoef(data, rowvar=False)
    np.testing.assert_allclose(corr_mat, expected_corr, rtol=1e-6)
    np.testing.assert_allclose(np.diag(corr_mat), np.ones(3), rtol=1e-6)


def test_mahalanobis_distance_properties():
    np.random.seed(42)
    ref = np.random.normal(loc=0.0, scale=1.0, size=(100, 2))
    mean_point = np.mean(ref, axis=0)
    dist_mean = mahalanobis_distance(mean_point, ref)
    assert dist_mean[0] < 0.2

    far_point = mean_point + 10.0
    dist_far = mahalanobis_distance(far_point, ref)
    assert dist_far[0] > dist_mean[0]


def test_pca_via_covariance():
    np.random.seed(42)
    X = np.random.randn(100, 5)
    pca_res = pca_via_covariance(X, n_components=2)

    assert pca_res["components"].shape == (5, 2)
    assert pca_res["transformed_data"].shape == (100, 2)
    assert len(pca_res["explained_variance"]) == 2
    assert len(pca_res["explained_variance_ratio"]) == 2

    dot_prod = np.dot(pca_res["components"][:, 0], pca_res["components"][:, 1])
    np.testing.assert_allclose(dot_prod, 0.0, atol=1e-6)


def test_error_handling():
    with pytest.raises(ValueError, match="matching lengths"):
        compute_covariance([1, 2, 3], [1, 2])

    with pytest.raises(ValueError, match="greater than ddof"):
        compute_covariance([1], [2], ddof=1)

    with pytest.raises(ValueError, match="2D array"):
        compute_covariance_matrix(np.array([1, 2, 3]))

    with pytest.raises(ValueError, match="strictly positive"):
        zero_var_cov = np.zeros((2, 2))
        covariance_to_correlation(zero_var_cov)

    with pytest.raises(ValueError, match="n_components must be positive"):
        data = np.random.randn(10, 3)
        pca_via_covariance(data, n_components=5)
