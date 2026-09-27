"""
Day 031: Big-O Time & Space Complexity Analysis
Demonstrates algorithmic time and space complexity trade-offs
using three approaches to the Two-Sum problem.
"""

import math
from typing import Any, Dict, List, Optional, Tuple


class OperationCounter:
    """Tracks operations (comparisons, allocations, lookups) to evaluate algorithmic metrics."""

    def __init__(self) -> None:
        self.comparisons: int = 0
        self.allocations: int = 0
        self.lookups: int = 0

    def reset(self) -> None:
        """Reset operation counters to zero."""
        self.comparisons = 0
        self.allocations = 0
        self.lookups = 0

    def count_comparison(self, count: int = 1) -> None:
        """Record element comparison operations."""
        self.comparisons += count

    def count_allocation(self, count: int = 1) -> None:
        """Record memory allocations (auxiliary space items)."""
        self.allocations += count

    def count_lookup(self, count: int = 1) -> None:
        """Record hash lookups or key accesses."""
        self.lookups += count

    def summary(self) -> Dict[str, int]:
        """Return summary dictionary of operation counts."""
        return {
            "comparisons": self.comparisons,
            "allocations": self.allocations,
            "lookups": self.lookups,
            "total_time_ops": self.comparisons + self.lookups,
            "auxiliary_space_ops": self.allocations,
        }


class TwoSumSolvers:
    """Implementations of Two-Sum algorithm demonstrating different Big-O trade-offs."""

    @staticmethod
    def brute_force(
        nums: List[int], target: int, counter: Optional[OperationCounter] = None
    ) -> Optional[Tuple[int, int]]:
        """Brute Force Approach: O(N^2) Time, O(1) Auxiliary Space."""
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if counter:
                    counter.count_comparison()
                if nums[i] + nums[j] == target:
                    return (i, j)
        return None

    @staticmethod
    def sorted_two_pointers(
        nums: List[int], target: int, counter: Optional[OperationCounter] = None
    ) -> Optional[Tuple[int, int]]:
        """Sorting + Two Pointers Approach: O(N log N) Time, O(N) Auxiliary Space."""
        if not nums:
            return None

        if counter:
            counter.count_allocation(len(nums))

        indexed_nums = [(num, i) for i, num in enumerate(nums)]
        indexed_nums.sort(key=lambda x: x[0])

        if counter:
            n = len(nums)
            est_sort_ops = int(n * math.log2(n)) if n > 1 else 1
            counter.count_comparison(est_sort_ops)

        left, right = 0, len(indexed_nums) - 1
        while left < right:
            if counter:
                counter.count_comparison()
            current_sum = indexed_nums[left][0] + indexed_nums[right][0]
            if current_sum == target:
                idx1 = indexed_nums[left][1]
                idx2 = indexed_nums[right][1]
                return (min(idx1, idx2), max(idx1, idx2))
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        return None

    @staticmethod
    def hash_map(
        nums: List[int], target: int, counter: Optional[OperationCounter] = None
    ) -> Optional[Tuple[int, int]]:
        """Hash Map Approach: O(N) Time, O(N) Auxiliary Space."""
        seen: Dict[int, int] = {}
        for i, num in enumerate(nums):
            complement = target - num
            if counter:
                counter.count_lookup()
            if complement in seen:
                return (seen[complement], i)
            seen[num] = i
            if counter:
                counter.count_allocation()
        return None


def analyze_complexity(nums: List[int], target: int) -> Dict[str, Dict[str, Any]]:
    """Executes all three solvers and collects complexity metrics."""
    counter = OperationCounter()

    counter.reset()
    res_brute = TwoSumSolvers.brute_force(nums, target, counter)
    metrics_brute = counter.summary()

    counter.reset()
    res_sort = TwoSumSolvers.sorted_two_pointers(nums, target, counter)
    metrics_sort = counter.summary()

    counter.reset()
    res_hash = TwoSumSolvers.hash_map(nums, target, counter)
    metrics_hash = counter.summary()

    return {
        "brute_force": {"result": res_brute, "metrics": metrics_brute},
        "sorted_two_pointers": {"result": res_sort, "metrics": metrics_sort},
        "hash_map": {"result": res_hash, "metrics": metrics_hash},
    }
