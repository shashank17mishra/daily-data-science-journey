from dataclasses import dataclass
import heapq
from typing import List, Optional, Tuple


@dataclass(frozen=True)
class Interval:
    """Represents a semi-open time interval [start, end)."""

    start: float
    end: float
    id: Optional[str] = None

    def __post_init__(self) -> None:
        if self.start >= self.end:
            raise ValueError(
                f"Invalid interval: start ({self.start}) must be strictly less than end ({self.end})."
            )

    @property
    def duration(self) -> float:
        """Calculates duration of the interval."""
        return self.end - self.start

    def overlaps(self, other: "Interval") -> bool:
        """Determines if this interval overlaps with another. Boundary contact is not overlap."""
        return max(self.start, other.start) < min(self.end, other.end)


def select_max_non_overlapping(intervals: List[Interval]) -> List[Interval]:
    """Selects maximum subset of non-overlapping intervals using greedy choice by end time.

    Time Complexity: O(N log N)
    Space Complexity: O(N)
    """
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda inv: (inv.end, inv.start))
    selected: List[Interval] = []
    last_end = float("-inf")

    for inv in sorted_intervals:
        if inv.start >= last_end:
            selected.append(inv)
            last_end = inv.end

    return selected


def min_removals_to_avoid_overlap(intervals: List[Interval]) -> int:
    """Calculates minimum removals required to eliminate all overlapping intervals."""
    if not intervals:
        return 0
    selected = select_max_non_overlapping(intervals)
    return len(intervals) - len(selected)


def min_resources_required(intervals: List[Interval]) -> Tuple[int, List[List[Interval]]]:
    """Determines minimum parallel resources (e.g. rooms) needed for all intervals.

    Time Complexity: O(N log N)
    Space Complexity: O(N)
    """
    if not intervals:
        return 0, []

    sorted_intervals = sorted(intervals, key=lambda inv: (inv.start, inv.end))
    heap: List[Tuple[float, int]] = []
    resource_assignments: List[List[Interval]] = []

    for inv in sorted_intervals:
        if heap and heap[0][0] <= inv.start:
            _, resource_idx = heapq.heappop(heap)
            resource_assignments[resource_idx].append(inv)
            heapq.heappush(heap, (inv.end, resource_idx))
        else:
            new_idx = len(resource_assignments)
            resource_assignments.append([inv])
            heapq.heappush(heap, (inv.end, new_idx))

    return len(resource_assignments), resource_assignments
