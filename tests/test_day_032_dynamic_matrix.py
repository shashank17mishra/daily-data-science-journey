import pytest
from learning.dsa.day_032_dynamic_matrix import DynamicMatrix


def test_init_valid():
    matrix = DynamicMatrix(3, 4, fill_value=1)
    assert matrix.shape == (3, 4)
    assert matrix.to_list() == [[1] * 4 for _ in range(3)]


def test_init_invalid():
    with pytest.raises(ValueError):
        DynamicMatrix(0, 5)
    with pytest.raises(ValueError):
        DynamicMatrix(3, -1)


def test_from_list_and_shape():
    grid = [[1, 2, 3], [4, 5, 6]]
    matrix = DynamicMatrix.from_list(grid)
    assert matrix.shape == (2, 3)
    assert matrix.get(0, 1) == 2
    assert matrix.get(1, 2) == 6


def test_from_list_invalid():
    with pytest.raises(ValueError):
        DynamicMatrix.from_list([])
    with pytest.raises(ValueError):
        DynamicMatrix.from_list([[1, 2], [3]])


def test_get_set_bounds():
    matrix = DynamicMatrix(2, 2, fill_value=0)
    matrix.set(1, 1, 9)
    assert matrix.get(1, 1) == 9

    with pytest.raises(IndexError):
        matrix.get(2, 0)
    with pytest.raises(IndexError):
        matrix.set(-1, 0, 5)


def test_resize_expand_and_truncate():
    grid = [[1, 2], [3, 4]]
    matrix = DynamicMatrix.from_list(grid)

    matrix.resize(3, 3, fill_value=0)
    assert matrix.shape == (3, 3)
    assert matrix.to_list() == [[1, 2, 0], [3, 4, 0], [0, 0, 0]]

    matrix.resize(1, 2)
    assert matrix.shape == (1, 2)
    assert matrix.to_list() == [[1, 2]]


def test_transpose():
    grid = [[1, 2, 3], [4, 5, 6]]
    matrix = DynamicMatrix.from_list(grid)
    matrix.transpose()
    assert matrix.shape == (3, 2)
    assert matrix.to_list() == [[1, 4], [2, 5], [3, 6]]


def test_rotate():
    grid = [[1, 2, 3], [4, 5, 6]]
    matrix = DynamicMatrix.from_list(grid)

    matrix.rotate(clockwise=True)
    assert matrix.shape == (3, 2)
    assert matrix.to_list() == [[4, 1], [5, 2], [6, 3]]

    matrix.rotate(clockwise=False)
    assert matrix.shape == (2, 3)
    assert matrix.to_list() == [[1, 2, 3], [4, 5, 6]]


def test_region_sum():
    grid = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    matrix = DynamicMatrix.from_list(grid)

    assert matrix.region_sum(0, 0, 2, 2) == 45
    assert matrix.region_sum(1, 1, 1, 1) == 5
    assert matrix.region_sum(1, 1, 2, 2) == 28


def test_region_sum_invalidation():
    grid = [[1, 2], [3, 4]]
    matrix = DynamicMatrix.from_list(grid)
    assert matrix.region_sum(0, 0, 1, 1) == 10

    matrix.set(0, 0, 10)
    assert matrix.region_sum(0, 0, 1, 1) == 19


def test_region_sum_invalid_coords():
    matrix = DynamicMatrix(3, 3, fill_value=1)
    with pytest.raises(ValueError):
        matrix.region_sum(2, 2, 1, 1)
