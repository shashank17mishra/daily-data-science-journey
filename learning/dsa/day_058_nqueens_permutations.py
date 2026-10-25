"""
Day 058: Backtracking - N-Queens and Permutations

This module implements classic backtracking algorithms:
1. NQueensSolver: Solves N-Queens board placement and bitmask solution counting.
2. PermutationGenerator: Generates standard permutations and unique permutations with duplicates.
"""

from typing import List


class NQueensSolver:
    """Solves N-Queens puzzle using state tracking and bitwise backtracking."""

    def __init__(self, n: int) -> None:
        if n < 1:
            raise ValueError("Board size 'n' must be a positive integer.")
        self.n = n

    def solve(self) -> List[List[str]]:
        """
        Finds all distinct placements of N queens on an NxN chessboard.

        Returns:
            List[List[str]]: List of valid board configurations.
        """
        results: List[List[str]] = []
        board = [["."] * self.n for _ in range(self.n)]
        cols: set = set()
        pos_diag: set = set()  # (row + col)
        neg_diag: set = set()  # (row - col)

        def backtrack(row: int) -> None:
            if row == self.n:
                results.append(["".join(r) for r in board])
                return

            for col in range(self.n):
                if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                    continue

                cols.add(col)
                pos_diag.add(row + col)
                neg_diag.add(row - col)
                board[row][col] = "Q"

                backtrack(row + 1)

                cols.remove(col)
                pos_diag.remove(row + col)
                neg_diag.remove(row - col)
                board[row][col] = "."

        backtrack(0)
        return results

    def count_solutions(self) -> int:
        """
        Counts total number of solutions using bitmasking.

        Returns:
            int: Number of valid placements.
        """
        count = 0
        limit = (1 << self.n) - 1

        def backtrack(cols: int, pos_diag: int, neg_diag: int) -> None:
            nonlocal count
            if cols == limit:
                count += 1
                return

            available_positions = limit & (~(cols | pos_diag | neg_diag))
            while available_positions:
                position = available_positions & -available_positions
                available_positions ^= position
                backtrack(
                    cols | position,
                    (pos_diag | position) << 1,
                    (neg_diag | position) >> 1,
                )

        backtrack(0, 0, 0)
        return count


class PermutationGenerator:
    """Generates permutations of sequences using depth-first search backtracking."""

    @staticmethod
    def permute(nums: List[int]) -> List[List[int]]:
        """
        Generates all possible permutations of a list of distinct integers.

        Args:
            nums: List of unique integers.

        Returns:
            List[List[int]]: All possible permutations.
        """
        results: List[List[int]] = []
        path: List[int] = []
        used = [False] * len(nums)

        def backtrack() -> None:
            if len(path) == len(nums):
                results.append(path.copy())
                return

            for i in range(len(nums)):
                if used[i]:
                    continue
                used[i] = True
                path.append(nums[i])

                backtrack()

                path.pop()
                used[i] = False

        backtrack()
        return results

    @staticmethod
    def permute_unique(nums: List[int]) -> List[List[int]]:
        """
        Generates all unique permutations of a list that may contain duplicate values.

        Args:
            nums: List of integers (duplicates allowed).

        Returns:
            List[List[int]]: All unique permutations.
        """
        results: List[List[int]] = []
        path: List[int] = []
        sorted_nums = sorted(nums)
        used = [False] * len(sorted_nums)

        def backtrack() -> None:
            if len(path) == len(sorted_nums):
                results.append(path.copy())
                return

            for i in range(len(sorted_nums)):
                if used[i]:
                    continue
                if i > 0 and sorted_nums[i] == sorted_nums[i - 1] and not used[i - 1]:
                    continue

                used[i] = True
                path.append(sorted_nums[i])

                backtrack()

                path.pop()
                used[i] = False

        backtrack()
        return results
