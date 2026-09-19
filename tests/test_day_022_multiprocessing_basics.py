"""
Tests for Day 022: Multiprocessing Basics
"""

import pytest
from learning.python.day_022_multiprocessing_basics import (
    compute_heavy_task,
    run_parallel_map,
    QueueProcessPipeline,
)


def multiply_by_two(x: int) -> int:
    return x * 2


def failing_func(x: int) -> int:
    if x == 0:
        raise ValueError("Cannot divide by zero")
    return 100 // x


def test_compute_heavy_task():
    assert compute_heavy_task(1) == 0
    assert compute_heavy_task(5) > 0


def test_run_parallel_map_empty():
    results = run_parallel_map(multiply_by_two, [])
    assert results == []


def test_run_parallel_map_execution():
    inputs = [1, 2, 3, 4, 5]
    results = run_parallel_map(multiply_by_two, inputs, num_processes=2)
    assert results == [2, 4, 6, 8, 10]


def test_queue_process_pipeline_basic():
    pipeline = QueueProcessPipeline(multiply_by_two, num_workers=2)
    pipeline.start()
    pipeline.submit_batch([10, 20, 30])
    results = pipeline.collect_results()

    # Process order might differ, so sort by input item
    sorted_results = sorted(results, key=lambda x: x[0])
    assert sorted_results == [
        (10, 20, None),
        (20, 40, None),
        (30, 60, None),
    ]


def test_queue_process_pipeline_error_handling():
    pipeline = QueueProcessPipeline(failing_func, num_workers=2)
    pipeline.start()
    pipeline.submit_batch([10, 0, 5])
    results = pipeline.collect_results()

    sorted_results = sorted(results, key=lambda x: x[0])
    assert sorted_results[0] == (0, None, "Cannot divide by zero")
    assert sorted_results[1] == (5, 20, None)
    assert sorted_results[2] == (10, 10, None)
