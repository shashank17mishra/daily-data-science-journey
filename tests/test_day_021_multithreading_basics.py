import time
import pytest
from learning.python.day_021_multithreading_basics import TaskProcessor


def sample_task(x: int, y: int) -> int:
    time.sleep(0.01)
    return x + y


def failing_task() -> None:
    raise ValueError("Task failed intentionally")


def test_invalid_worker_count():
    with pytest.raises(ValueError, match="at least 1"):
        TaskProcessor(num_workers=0)


def test_submit_before_start():
    processor = TaskProcessor(num_workers=2)
    with pytest.raises(RuntimeError, match="not running"):
        processor.submit(sample_task, 1, 2)


def test_successful_task_execution():
    processor = TaskProcessor(num_workers=3)
    processor.start()

    for i in range(5):
        processor.submit(sample_task, i, i * 2)

    processor.stop()
    results = processor.get_results()

    assert len(results) == 5
    assert sorted(results) == [0, 3, 6, 9, 12]
    assert len(processor.get_errors()) == 0


def test_error_handling_in_worker():
    processor = TaskProcessor(num_workers=2)
    processor.start()

    processor.submit(sample_task, 2, 3)
    processor.submit(failing_task)

    processor.stop()

    results = processor.get_results()
    errors = processor.get_errors()

    assert len(results) == 1
    assert results[0] == 5
    assert len(errors) == 1
    assert isinstance(errors[0][1], ValueError)


def test_multiple_starts_and_stops():
    processor = TaskProcessor(num_workers=2)
    processor.start()
    processor.start()

    processor.submit(sample_task, 10, 20)
    processor.stop()
    processor.stop()

    assert processor.get_results() == [30]
