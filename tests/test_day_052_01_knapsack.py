"""Unit tests for 0/1 Knapsack DP implementations."""

import pytest
from learning.dsa.day_052_01_knapsack import (
    knapsack_01_memoization,
    knapsack_01_bottom_up,
    knapsack_01_space_optimized,
)


def test_knapsack_standard_cases():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5

    expected_val = 7
    assert knapsack_01_memoization(weights, values, capacity) == expected_val
    max_val, indices = knapsack_01_bottom_up(weights, values, capacity)
    assert max_val == expected_val
    assert knapsack_01_space_optimized(weights, values, capacity) == expected_val

    total_weight = sum(weights[i] for i in indices)
    total_value = sum(values[i] for i in indices)
    assert total_weight <= capacity
    assert total_value == expected_val


def test_knapsack_all_fit():
    weights = [1, 2, 3]
    values = [10, 20, 30]
    capacity = 10

    assert knapsack_01_memoization(weights, values, capacity) == 60
    val, indices = knapsack_01_bottom_up(weights, values, capacity)
    assert val == 60
    assert indices == [0, 1, 2]
    assert knapsack_01_space_optimized(weights, values, capacity) == 60


def test_knapsack_none_fit():
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 5

    assert knapsack_01_memoization(weights, values, capacity) == 0
    val, indices = knapsack_01_bottom_up(weights, values, capacity)
    assert val == 0
    assert indices == []
    assert knapsack_01_space_optimized(weights, values, capacity) == 0


def test_knapsack_zero_capacity_and_empty_inputs():
    assert knapsack_01_memoization([], [], 10) == 0
    val, indices = knapsack_01_bottom_up([], [], 10)
    assert val == 0 and indices == []
    assert knapsack_01_space_optimized([], [], 10) == 0

    weights = [1, 2, 3]
    values = [10, 20, 30]
    assert knapsack_01_memoization(weights, values, 0) == 0
    val, indices = knapsack_01_bottom_up(weights, values, 0)
    assert val == 0 and indices == []
    assert knapsack_01_space_optimized(weights, values, 0) == 0


def test_knapsack_invalid_inputs():
    with pytest.raises(ValueError, match="Weights and values must have the same length"):
        knapsack_01_memoization([1, 2], [10], 5)

    with pytest.raises(ValueError, match="Capacity cannot be negative"):
        knapsack_01_bottom_up([1], [10], -1)

    with pytest.raises(ValueError, match="Weights cannot contain negative values"):
        knapsack_01_space_optimized([-1, 2], [10, 20], 5)

    with pytest.raises(ValueError, match="Values cannot contain negative values"):
        knapsack_01_memoization([1, 2], [-10, 20], 5)
