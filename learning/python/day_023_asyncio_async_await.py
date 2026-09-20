"""
Day 023: Asyncio & Async/Await
Concurrent Task Execution with Concurrency Control and Retries.
"""

import asyncio
import logging
from typing import Any, Callable, Coroutine, List, Optional, Tuple, TypeVar

T = TypeVar("T")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def async_retry(
    coro_func: Callable[..., Coroutine[Any, Any, T]],
    *args: Any,
    retries: int = 3,
    delay: float = 0.1,
    backoff: float = 2.0,
    **kwargs: Any,
) -> T:
    """Executes an async function with retry logic and exponential backoff."""
    current_delay = delay
    last_exception: Optional[Exception] = None

    for attempt in range(1, retries + 1):
        try:
            return await coro_func(*args, **kwargs)
        except Exception as exc:
            last_exception = exc
            if attempt == retries:
                logger.error(f"Task failed after {retries} attempts: {exc}")
                raise exc
            logger.warning(
                f"Attempt {attempt} failed ({exc}). Retrying in {current_delay:.2f}s..."
            )
            await asyncio.sleep(current_delay)
            current_delay *= backoff

    if last_exception:
        raise last_exception
    raise RuntimeError("Unexpected error in async_retry")


class AsyncTaskPool:
    """Manages concurrent execution of asynchronous tasks with rate limiting."""

    def __init__(self, max_concurrency: int = 5):
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be at least 1")
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def _worker(
        self, coro_func: Callable[..., Coroutine[Any, Any, T]], *args: Any, **kwargs: Any
    ) -> Tuple[bool, Any]:
        async with self.semaphore:
            try:
                result = await coro_func(*args, **kwargs)
                return True, result
            except Exception as exc:
                return False, exc

    async def map(
        self, 
        coro_func: Callable[..., Coroutine[Any, Any, T]], 
        items: List[Any], 
        return_exceptions: bool = True
    ) -> List[Any]:
        """Applies coro_func to items concurrently while respecting max_concurrency."""
        tasks = [self._worker(coro_func, item) for item in items]
        raw_results = await asyncio.gather(*tasks)

        results = []
        for success, val in raw_results:
            if success:
                results.append(val)
            else:
                if return_exceptions:
                    results.append(val)
                else:
                    raise val
        return results
