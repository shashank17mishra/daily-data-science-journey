"""
Tests for Day 058: Backtracking - N-Queens & Permutations
"""

import pytest
from learning.dsa.day_058_nqueens_permutations import (
    NQueensSolver,
    PermutationGenerator,
)


def is_valid_nqueens_board(board: list[str]) -> bool:
    """Helper to verify N-Queens placement validity."""
    n = len(board)
    queens = []
    for r in range(n):
        for c in range(n):
            if board[r][c] == "Q":
                queens.append((r, c))

    if len(queens) != n:
        return False

    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            r1, c1 = queens[i]
            r2, c2 = queens[j]
            if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                return False
    return True


def test_nqueens_invalid_n():
    with pytest.raises(ValueError):
        NQueensSolver(0)
    with pytest.raises(ValueError):
        NQueensSolver(-3)


def test_nqueens_n1():
    solver = NQueensSolver(1)
    solutions = solver.solve()
    assert solutions == [["Q"]]
    assert solver.count_solutions() == 1


def test_nqueens_n2_n3():
    for n in (2, 3):
        solver = NQueensSolver(n)
        assert solver.solve() == []
        assert solver.count_solutions() == 0


def test_nqueens_n4():
    solver = NQueensSolver(4)
    solutions = solver.solve()
    assert len(solutions) == 2
    assert solver.count_solutions() == 2
    for board in solutions:
        assert is_valid_nqueens_board(board)


def test_nqueens_n8_count():
    solver = NQueensSolver(8)
    solutions = solver.solve()
    assert len(solutions) == 92
    assert solver.count_solutions() == 92
    for board in solutions[:5]:
        assert is_valid_nqueens_board(board)


def test_permute_empty_and_single():
    assert PermutationGenerator.permute([]) == [[]]
    assert PermutationGenerator.permute([42]) == [[42]]


def test_permute_distinct():
    nums = [1, 2, 3]
    perms = PermutationGenerator.permute(nums)
    assert len(perms) == 6
    expected = [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 1, 2],
        [3, 2, 1],
    ]
    assert sorted(perms) == sorted(expected)


def test_permute_unique_duplicates():
    nums = [1, 1, 2]
    perms = PermutationGenerator.permute_unique(nums)
    assert len(perms) == 3
    expected = [
        [1, 1, 2],
        [1, 2, 1],
        [2, 1, 1],
    ]
    assert sorted(perms) == sorted(expected)


def test_permute_unique_all_same():
    nums = [7, 7, 7, 7]
    perms = PermutationGenerator.permute_unique(nums)
    assert perms == [[7, 7, 7, 7]]


def test_permute_unique_unordered_input():
    nums = [2, 1, 2]
    perms = PermutationGenerator.permute_unique(nums)
    assert len(perms) == 3
    expected = [
        [1, 2, 2],
        [2, 1, 2],
        [2, 2, 1],
    ]
    assert sorted(perms) == sorted(expected)
