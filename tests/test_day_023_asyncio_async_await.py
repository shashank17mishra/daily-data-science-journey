import asyncio
import pytest
from learning.python.day_023_asyncio_async_await import (
    async_retry,
    AsyncTaskPool,
)


def test_async_retry_success():
    call_count = 0

    async def sample_coro(val):
        nonlocal call_count
        call_count += 1
        return val * 2

    result = asyncio.run(async_retry(sample_coro, 5, retries=3, delay=0.01))
    assert result == 10
    assert call_count == 1


def test_async_retry_failure_then_success():
    call_count = 0

    async def flaky_coro(val):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Temporary failure")
        return val + 10

    result = asyncio.run(
        async_retry(flaky_coro, 5, retries=3, delay=0.01, backoff=1.0)
    )
    assert result == 15
    assert call_count == 3


def test_async_retry_max_retries_exceeded():
    async def always_failing():
        raise RuntimeError("Persistent failure")

    with pytest.raises(RuntimeError) as exc_info:
        asyncio.run(async_retry(always_failing, retries=2, delay=0.01))
    assert "Persistent failure" in str(exc_info.value)


def test_async_task_pool_concurrency():
    active_count = 0
    max_active_observed = 0

    async def slow_task(x):
        nonlocal active_count, max_active_observed
        active_count += 1
        if active_count > max_active_observed:
            max_active_observed = active_count
        await asyncio.sleep(0.05)
        active_count -= 1
        return x * 2

    async def run_test():
        pool = AsyncTaskPool(max_concurrency=2)
        results = await pool.map(slow_task, list(range(5)))
        return results

    results = asyncio.run(run_test())
    assert results == [0, 2, 4, 6, 8]
    assert max_active_observed <= 2


def test_async_task_pool_exception_handling():
    async def task_with_error(x):
        if x == 2:
            raise ValueError("Error on 2")
        return x * 10

    async def run_test():
        pool = AsyncTaskPool(max_concurrency=3)
        return await pool.map(task_with_error, [1, 2, 3], return_exceptions=True)

    results = asyncio.run(run_test())
    assert results[0] == 10
    assert isinstance(results[1], ValueError)
    assert str(results[1]) == "Error on 2"
    assert results[2] == 30


def test_async_task_pool_raises_exception():
    async def task_with_error(x):
        if x == 2:
            raise ValueError("Error on 2")
        return x * 10

    async def run_test():
        pool = AsyncTaskPool(max_concurrency=3)
        await pool.map(task_with_error, [1, 2, 3], return_exceptions=False)

    with pytest.raises(ValueError):
        asyncio.run(run_test())


def test_async_task_pool_invalid_concurrency():
    with pytest.raises(ValueError):
        AsyncTaskPool(max_concurrency=0)
