import pytest
from learning.dsa.day_043_monotonic_deque import MonotonicQueue, sliding_window_maximum

def test_monotonic_queue_basic_operations():
    mq = MonotonicQueue()
    
    # Test empty queue exceptions
    with pytest.raises(IndexError):
        mq.pop()
    with pytest.raises(IndexError):
        mq.max()
        
    # Push elements and verify max
    mq.push(1)
    assert mq.max() == 1
    
    mq.push(3)
    assert mq.max() == 3
    
    mq.push(2)
    assert mq.max() == 3
    
    # Pop elements and verify max updates
    assert mq.pop() == 1
    assert mq.max() == 3
    
    assert mq.pop() == 3
    assert mq.max() == 2
    
    assert mq.pop() == 2
    assert len(mq) == 0

def test_sliding_window_maximum_standard():
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    expected = [3, 3, 5, 5, 6, 7]
    assert sliding_window_maximum(nums, k) == expected

def test_sliding_window_maximum_edge_cases():
    # Empty input
    assert sliding_window_maximum([], 3) == []
    
    # Window size 0 or negative
    assert sliding_window_maximum([1, 2, 3], 0) == []
    
    # Window size larger than array length
    assert sliding_window_maximum([1, 5, 3], 5) == [5]
    
    # Window size equal to array length
    assert sliding_window_maximum([1, 5, 3], 3) == [5]
    
    # Single element array
    assert sliding_window_maximum([42], 1) == [42]

def test_sliding_window_all_decreasing():
    nums = [5, 4, 3, 2, 1]
    k = 2
    expected = [5, 4, 3, 2]
    assert sliding_window_maximum(nums, k) == expected

def test_sliding_window_all_increasing():
    nums = [1, 2, 3, 4, 5]
    k = 2
    expected = [2, 3, 4, 5]
    assert sliding_window_maximum(nums, k) == expected
