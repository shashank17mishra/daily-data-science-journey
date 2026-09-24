import pytest
from learning.python.day_028_stream_processor import (
    StreamProcessor,
    Transaction,
    compose,
    filter_high_value_transactions,
    filter_category
)

def test_sliding_window_average():
    data = [10, 20, 30, 40, 50]
    # Window size 3:
    # [10] -> 10.0
    # [10, 20] -> 15.0
    # [10, 20, 30] -> 20.0
    # [20, 30, 40] -> 30.0
    # [30, 40, 50] -> 40.0
    expected = [10.0, 15.0, 20.0, 30.0, 40.0]
    result = list(StreamProcessor.sliding_window_average(data, 3))
    assert result == expected

def test_sliding_window_average_invalid_window():
    with pytest.raises(ValueError):
        list(StreamProcessor.sliding_window_average([1, 2, 3], 0))
    with pytest.raises(ValueError):
        list(StreamProcessor.sliding_window_average([1, 2, 3], -5))

def test_running_frequencies():
    data = ['apple', 'banana', 'apple', 'cherry', 'banana']
    expected = [
        {'apple': 1},
        {'apple': 1, 'banana': 1},
        {'apple': 2, 'banana': 1},
        {'apple': 2, 'banana': 1, 'cherry': 1},
        {'apple': 2, 'banana': 2, 'cherry': 1}
    ]
    result = list(StreamProcessor.running_frequencies(data))
    assert result == expected

def test_group_consecutive():
    data = [1, 1, 2, 2, 2, 3, 1, 1]
    # Group consecutive identical numbers
    result = list(StreamProcessor.group_consecutive(data, lambda x: x))
    expected = [
        (1, [1, 1]),
        (2, [2, 2, 2]),
        (3, [3]),
        (1, [1, 1])
    ]
    assert result == expected

def test_batch_stream():
    data = range(10)
    result = list(StreamProcessor.batch_stream(data, 3))
    expected = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    assert result == expected

    with pytest.raises(ValueError):
        list(StreamProcessor.batch_stream(data, 0))

def test_compose():
    add_two = lambda x: x + 2
    multiply_three = lambda x: x * 3
    # compose(f, g)(x) -> f(g(x))
    # multiply_three(add_two(5)) -> (5 + 2) * 3 = 21
    pipeline = compose(multiply_three, add_two)
    assert pipeline(5) == 21

def test_transaction_pipeline():
    transactions = [
        Transaction("t1", "user1", 50.0, "electronics"),
        Transaction("t2", "user2", 150.0, "electronics"),
        Transaction("t3", "user1", 200.0, "groceries"),
        Transaction("t4", "user3", 300.0, "electronics"),
    ]
    
    # Filter high value (> 100) and category 'electronics'
    high_val_filter = filter_high_value_transactions
    electronics_filter = filter_category("electronics")
    
    # Combine filters using functional composition
    # Note: filter returns an iterator, so we compose the filter applications
    pipeline = compose(electronics_filter, high_val_filter)
    
    filtered_txs = list(pipeline(transactions))
    assert len(filtered_txs) == 2
    assert filtered_txs[0].transaction_id == "t2"
    assert filtered_txs[1].transaction_id == "t4"
