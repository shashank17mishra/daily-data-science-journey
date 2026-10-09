from collections import deque
from typing import Any, List

class MonotonicQueue:
    """
    A queue that supports push, pop, and retrieving the maximum element
    in O(1) amortized time using a monotonic decreasing deque.
    """
    def __init__(self) -> None:
        self._queue = deque()
        self._max_deque = deque()

    def push(self, val: Any) -> None:
        """
        Pushes an element to the back of the queue.
        Maintains the monotonic decreasing property of the max deque.
        """
        self._queue.append(val)
        # Maintain decreasing order in the max deque
        while self._max_deque and self._max_deque[-1] < val:
            self._max_deque.pop()
        self._max_deque.append(val)

    def pop(self) -> Any:
        """
        Pops the front element of the queue and returns it.
        Updates the max deque if the popped element was the current maximum.
        """
        if not self._queue:
            raise IndexError("pop from empty queue")
        val = self._queue.popleft()
        if val == self._max_deque[0]:
            self._max_deque.popleft()
        return val

    def max(self) -> Any:
        """
        Returns the maximum element currently in the queue in O(1) time.
        """
        if not self._max_deque:
            raise IndexError("max from empty queue")
        return self._max_deque[0]

    def __len__(self) -> int:
        return len(self._queue)


def sliding_window_maximum(nums: List[int], k: int) -> List[int]:
    """
    Finds the maximum value in each sliding window of size k.
    Uses MonotonicQueue to achieve O(N) time complexity.
    """
    if not nums or k <= 0:
        return []
    if k > len(nums):
        k = len(nums)

    mq = MonotonicQueue()
    result = []

    # Initialize the first window
    for i in range(k):
        mq.push(nums[i])
    result.append(mq.max())

    # Slide the window across the array
    for i in range(k, len(nums)):
        mq.pop()
        mq.push(nums[i])
        result.append(mq.max())

    return result
