"""Indexed Min-Heap implementation with dynamic key updates and fast lookup.

This module provides an Indexed Priority Queue (Indexed Min-Heap) supporting
O(log N) insertions, deletions, and priority updates, alongside O(1) key
containment checks and priority lookups.
"""

from typing import Any, Dict, List, Tuple


class IndexedMinHeap:
    """A binary min-heap supporting key-based operations and dynamic priority updates."""

    def __init__(self) -> None:
        # Heap array stores tuples of (key, priority)
        self._heap: List[Tuple[Any, float]] = []
        # Mapping from key to index in self._heap
        self._position_map: Dict[Any, int] = {}

    def __len__(self) -> int:
        return len(self._heap)

    def is_empty(self) -> bool:
        """Check if the heap contains no elements."""
        return len(self._heap) == 0

    def contains(self, key: Any) -> bool:
        """Check whether a key exists in the heap in O(1) time."""
        return key in self._position_map

    def get_priority(self, key: Any) -> float:
        """Get the current priority of a key in O(1) time."""
        if key not in self._position_map:
            raise KeyError(f"Key '{key}' not found in heap.")
        idx = self._position_map[key]
        return self._heap[idx][1]

    def peek(self) -> Tuple[Any, float]:
        """Return the (key, priority) tuple with the minimum priority without removing it."""
        if self.is_empty():
            raise IndexError("Peek from an empty heap.")
        return self._heap[0]

    def push(self, key: Any, priority: float) -> None:
        """Insert a new key with priority into the heap in O(log N) time."""
        if key in self._position_map:
            raise ValueError(f"Key '{key}' already exists in heap.")

        idx = len(self._heap)
        self._heap.append((key, float(priority)))
        self._position_map[key] = idx
        self._sift_up(idx)

    def pop(self) -> Tuple[Any, float]:
        """Remove and return the (key, priority) tuple with minimum priority in O(log N) time."""
        if self.is_empty():
            raise IndexError("Pop from an empty heap.")

        min_item = self._heap[0]
        last_item = self._heap.pop()
        del self._position_map[min_item[0]]

        if self._heap:
            self._heap[0] = last_item
            self._position_map[last_item[0]] = 0
            self._sift_down(0)

        return min_item

    def update_priority(self, key: Any, new_priority: float) -> None:
        """Update priority of an existing key and restore heap property in O(log N) time."""
        if key not in self._position_map:
            raise KeyError(f"Key '{key}' not found in heap.")

        idx = self._position_map[key]
        old_priority = self._heap[idx][1]
        new_prio_float = float(new_priority)
        self._heap[idx] = (key, new_prio_float)

        if new_prio_float < old_priority:
            self._sift_up(idx)
        elif new_prio_float > old_priority:
            self._sift_down(idx)

    def delete(self, key: Any) -> Tuple[Any, float]:
        """Remove an arbitrary key from the heap in O(log N) time."""
        if key not in self._position_map:
            raise KeyError(f"Key '{key}' not found in heap.")

        idx = self._position_map[key]
        item = self._heap[idx]

        if idx == len(self._heap) - 1:
            self._heap.pop()
            del self._position_map[key]
        else:
            last_item = self._heap.pop()
            del self._position_map[key]
            self._heap[idx] = last_item
            self._position_map[last_item[0]] = idx

            # Balance position after replacement
            self._sift_down(idx)
            self._sift_up(idx)

        return item

    def _sift_up(self, idx: int) -> None:
        """Bubble element up to restore min-heap property."""
        while idx > 0:
            parent_idx = (idx - 1) // 2
            if self._heap[idx][1] < self._heap[parent_idx][1]:
                self._swap(idx, parent_idx)
                idx = parent_idx
            else:
                break

    def _sift_down(self, idx: int) -> None:
        """Bubble element down to restore min-heap property."""
        size = len(self._heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx

            if left < size and self._heap[left][1] < self._heap[smallest][1]:
                smallest = left
            if right < size and self._heap[right][1] < self._heap[smallest][1]:
                smallest = right

            if smallest != idx:
                self._swap(idx, smallest)
                idx = smallest
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        """Swap heap array elements at indices i and j and sync position index map."""
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self._position_map[self._heap[i][0]] = i
        self._position_map[self._heap[j][0]] = j
