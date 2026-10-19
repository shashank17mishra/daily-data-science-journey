"""0/1 Knapsack Problem implementation with top-down, bottom-up, and space-optimized DP solutions."""

from typing import List, Tuple


def _validate_inputs(weights: List[int], values: List[int], capacity: int) -> None:
    """Validate knapsack input arguments.

    Raises:
        ValueError: If array lengths mismatch, capacity is negative, or weights/values contain negative numbers.
    """
    if len(weights) != len(values):
        raise ValueError("Weights and values must have the same length.")
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    if any(w < 0 for w in weights):
        raise ValueError("Weights cannot contain negative values.")
    if any(v < 0 for v in values):
        raise ValueError("Values cannot contain negative values.")


def knapsack_01_memoization(weights: List[int], values: List[int], capacity: int) -> int:
    """Solve 0/1 Knapsack using top-down recursion with memoization.

    Args:
        weights: List of item weights.
        values: List of item values.
        capacity: Maximum capacity of the knapsack.

    Returns:
        Maximum total value attainable.
    """
    _validate_inputs(weights, values, capacity)
    if not weights or capacity == 0:
        return 0

    memo = {}

    def solve(index: int, rem_capacity: int) -> int:
        if index < 0 or rem_capacity == 0:
            return 0
        state = (index, rem_capacity)
        if state in memo:
            return memo[state]

        max_val = solve(index - 1, rem_capacity)

        if weights[index] <= rem_capacity:
            include_val = values[index] + solve(index - 1, rem_capacity - weights[index])
            max_val = max(max_val, include_val)

        memo[state] = max_val
        return max_val

    return solve(len(weights) - 1, capacity)


def knapsack_01_bottom_up(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """Solve 0/1 Knapsack using 2D bottom-up dynamic programming with item reconstruction.

    Args:
        weights: List of item weights.
        values: List of item values.
        capacity: Maximum capacity of the knapsack.

    Returns:
        Tuple of (maximum_value, list_of_selected_item_indices).
    """
    _validate_inputs(weights, values, capacity)
    n = len(weights)
    if n == 0 or capacity == 0:
        return 0, []

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        for c in range(1, capacity + 1):
            if w <= c:
                dp[i][c] = max(dp[i - 1][c], v + dp[i - 1][c - w])
            else:
                dp[i][c] = dp[i - 1][c]

    max_value = dp[n][capacity]

    selected_indices = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            selected_indices.append(i - 1)
            c -= weights[i - 1]

    selected_indices.reverse()
    return max_value, selected_indices


def knapsack_01_space_optimized(weights: List[int], values: List[int], capacity: int) -> int:
    """Solve 0/1 Knapsack using 1D space-optimized dynamic programming.

    Args:
        weights: List of item weights.
        values: List of item values.
        capacity: Maximum capacity of the knapsack.

    Returns:
        Maximum total value attainable.
    """
    _validate_inputs(weights, values, capacity)
    if not weights or capacity == 0:
        return 0

    dp = [0] * (capacity + 1)

    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], v + dp[c - w])

    return dp[capacity]
