# Day 057: Greedy Interval Scheduling

## Overview
Implements classical greedy algorithms for interval scheduling, including activity selection (maximizing non-overlapping intervals), minimum interval removals to eliminate overlap, and minimum resource allocation (interval partitioning).

## Objectives
- Understand algorithmic mechanics of Greedy Interval Scheduling.
- Implement unit tests for edge cases.

## Key Concepts
Greedy Interval Scheduling algorithms rely on local optimal choices to find global solutions:

1. **Activity Selection Problem (`select_max_non_overlapping`)**:
   - **Strategy**: Sort intervals by end time `(inv.end, inv.start)`. Iterate and pick the next interval whose start time is greater than or equal to the end time of the last selected interval.
   - **Optimality**: Selecting the earliest finishing interval leaves maximum available time for remaining intervals.
   - **Complexity**: O(N log N) due to sorting, O(N) auxiliary space.

2. **Minimum Interval Removals (`min_removals_to_avoid_overlap`)**:
   - Minimizing removals is directly equivalent to `Total Intervals - Maximum Compatible Set Size`.

3. **Interval Partitioning / Room Allocation (`min_resources_required`)**:
   - **Strategy**: Sort intervals by start time. Maintain a min-heap storing the end times of currently active resources.
   - If the earliest available resource becomes free before or at the current interval's start time, re-assign that resource and update its end time in the min-heap. Otherwise, allocate a new resource.
   - **Complexity**: O(N log N) sorting + O(N log K) min-heap operations, where K is the number of parallel resources required.
