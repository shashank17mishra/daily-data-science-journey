"""
Day 051: Dynamic Programming - 1D Dynamic Programming Algorithms

This module implements advanced 1D Dynamic Programming solutions for:
1. Decode Ways with Wildcards (Decode Ways II)
2. Partition Array for Maximum Sum
3. Minimum Travel Cost Optimization
"""

from typing import List


class Advanced1DDP:
    """Collection of advanced 1D Dynamic Programming algorithms."""

    @staticmethod
    def num_decodings(s: str) -> int:
        """
        Calculates total ways to decode a message string containing digits
        and wildcard characters ('*').

        '1'-'9' map to 'A'-'I'.
        '10'-'19' map to 'J'-'S'.
        '20'-'26' map to 'T'-'Z'.
        '*' can represent any digit from '1' to '9'.

        Time Complexity: O(N)
        Space Complexity: O(1)

        Args:
            s: Input string containing digits and '*'

        Returns:
            Number of valid decodings modulo 10^9 + 7.
        """
        if not s or s[0] == '0':
            return 0

        MOD = 10**9 + 7

        def single_ways(c: str) -> int:
            if c == '0':
                return 0
            if c == '*':
                return 9
            return 1

        def pair_ways(c1: str, c2: str) -> int:
            if c1 == '*' and c2 == '*':
                return 15  # 11-19 (9) + 21-26 (6)
            if c1 == '*':
                val = int(c2)
                return 2 if val <= 6 else 1
            if c2 == '*':
                if c1 == '1':
                    return 9
                if c1 == '2':
                    return 6
                return 0
            val = int(c1 + c2)
            return 1 if 10 <= val <= 26 else 0

        n = len(s)
        prev2 = 1
        prev1 = single_ways(s[0])

        for i in range(2, n + 1):
            curr_c = s[i - 1]
            prev_c = s[i - 2]

            curr = (
                single_ways(curr_c) * prev1 + pair_ways(prev_c, curr_c) * prev2
            ) % MOD

            prev2 = prev1
            prev1 = curr

        return prev1

    @staticmethod
    def max_sum_after_partitioning(arr: List[int], k: int) -> int:
        """
        Partitions an array into contiguous subarrays of length at most k.
        After partitioning, each element in a subarray is updated to the maximum
        value in that subarray. Returns the maximum sum possible.

        Time Complexity: O(N * K)
        Space Complexity: O(N)

        Args:
            arr: List of integers.
            k: Maximum partition size (k >= 1).

        Returns:
            Maximum sum after optimal partitioning.
        """
        if not arr or k <= 0:
            return 0

        n = len(arr)
        dp = [0] * (n + 1)

        for i in range(1, n + 1):
            cur_max = 0
            for len_sub in range(1, min(i, k) + 1):
                cur_max = max(cur_max, arr[i - len_sub])
                dp[i] = max(dp[i], dp[i - len_sub] + cur_max * len_sub)

        return dp[n]

    @staticmethod
    def min_cost_tickets(days: List[int], costs: List[int]) -> int:
        """
        Calculates minimum travel cost using 1-day, 7-day, or 30-day passes.

        Time Complexity: O(max_day)
        Space Complexity: O(max_day)

        Args:
            days: Sorted list of travel days (1-indexed).
            costs: List of 3 pass costs [1-day, 7-day, 30-day].

        Returns:
            Minimum travel cost.
        """
        if not days or not costs or len(costs) != 3:
            return 0

        travel_days = set(days)
        last_day = days[-1]
        dp = [0] * (last_day + 1)

        for day in range(1, last_day + 1):
            if day not in travel_days:
                dp[day] = dp[day - 1]
            else:
                cost_1 = dp[day - 1] + costs[0]
                cost_7 = dp[max(0, day - 7)] + costs[1]
                cost_30 = dp[max(0, day - 30)] + costs[2]
                dp[day] = min(cost_1, cost_7, cost_30)

        return dp[last_day]
