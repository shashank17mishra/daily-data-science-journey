"""
Day 053: Dynamic Programming - Longest Common Subsequence (LCS)

This module provides dynamic programming methods for solving the Longest
Common Subsequence (LCS) problem. It includes standard 2D DP table construction,
space-optimized 1D DP, single sequence reconstruction, and retrieval of all
distinct longest common subsequences.
"""

from typing import Set


class LongestCommonSubsequence:
    """Class encapsulating LCS algorithms and helper utilities."""

    @staticmethod
    def lcs_length(text1: str, text2: str) -> int:
        """Compute the length of the LCS using a standard 2D DP table.

        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]

    @staticmethod
    def lcs_length_optimized(text1: str, text2: str) -> int:
        """Compute the length of the LCS using 1D space optimization.

        Time Complexity: O(m * n)
        Space Complexity: O(min(m, n))
        """
        if len(text1) < len(text2):
            text1, text2 = text2, text1

        m, n = len(text1), len(text2)
        dp = [0] * (n + 1)

        for i in range(1, m + 1):
            prev = 0
            for j in range(1, n + 1):
                temp = dp[j]
                if text1[i - 1] == text2[j - 1]:
                    dp[j] = prev + 1
                else:
                    dp[j] = max(dp[j], dp[j - 1])
                prev = temp

        return dp[n]

    @staticmethod
    def get_one_lcs(text1: str, text2: str) -> str:
        """Reconstruct one LCS string from two input strings.

        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        lcs_chars = []
        i, j = m, n
        while i > 0 and j > 0:
            if text1[i - 1] == text2[j - 1]:
                lcs_chars.append(text1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] >= dp[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return "".join(reversed(lcs_chars))

    @staticmethod
    def get_all_lcs(text1: str, text2: str) -> Set[str]:
        """Extract all unique longest common subsequences.

        Time Complexity: O(m * n + K) where K is path search space
        Space Complexity: O(m * n + K)
        """
        m, n = len(text1), len(text2)
        if m == 0 or n == 0:
            return {""}

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        memo = {}

        def backtrack(i: int, j: int) -> Set[str]:
            if i == 0 or j == 0:
                return {""}
            if (i, j) in memo:
                return memo[(i, j)]

            res = set()
            if text1[i - 1] == text2[j - 1]:
                sub_res = backtrack(i - 1, j - 1)
                for seq in sub_res:
                    res.add(seq + text1[i - 1])
            else:
                if dp[i - 1][j] >= dp[i][j - 1]:
                    res.update(backtrack(i - 1, j))
                if dp[i][j - 1] >= dp[i - 1][j]:
                    res.update(backtrack(i, j - 1))

            memo[(i, j)] = res
            return res

        return backtrack(m, n)
