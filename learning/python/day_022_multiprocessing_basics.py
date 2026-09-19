"""
Day 022: Multiprocessing Basics in Python

This module demonstrates key multiprocessing concepts:
- Utilizing CPU-bound parallel execution with `multiprocessing.Pool`
- Inter-process communication using `multiprocessing.Queue` and `multiprocessing.Process`
- Poison pill termination pattern for graceful process shutdown
"""

import multiprocessing as mp
from typing import Any, Callable, List, Optional, Tuple


def compute_heavy_task(n: int) -> int:
    """A CPU-bound task: calculate sum of prime factors up to n."""
    if n <= 1:
        return 0
    total = 0
    for i in range(2, n + 1):
        temp = i
        d = 2
        while d * d <= temp:
            if temp % d == 0:
                total += d
                while temp % d == 0:
                    temp //= d
            d += 1
        if temp > 1:
            total += temp
    return total


def run_parallel_map(
    func: Callable[[Any], Any],
    items: List[Any],
    num_processes: Optional[int] = None
) -> List[Any]:
    """Executes a function over a list of items in parallel using multiprocessing.Pool.

    Args:
        func: A top-level function to apply to each item.
        items: Input data items.
        num_processes: Number of process workers (defaults to CPU count).

    Returns:
        List of processed results maintaining input order.
    """
    if not items:
        return []
    workers = num_processes or max(1, mp.cpu_count())
    with mp.Pool(processes=workers) as pool:
        results = pool.map(func, items)
    return results


def _worker_loop(
    task_queue: mp.Queue,
    result_queue: mp.Queue,
    func: Callable[[Any], Any]
) -> None:
    """Worker loop process consuming tasks and pushing results until poison pill received."""
    while True:
        item = task_queue.get()
        if item is None:  # Poison pill signal to terminate worker
            break
        try:
            res = func(item)
            result_queue.put((item, res, None))
        except Exception as e:
            result_queue.put((item, None, str(e)))


class QueueProcessPipeline:
    """Demonstrates process spawning and queue management for worker communication."""

    def __init__(self, func: Callable[[Any], Any], num_workers: int = 2):
        self.func = func
        self.num_workers = max(1, num_workers)
        self.task_queue: mp.Queue = mp.Queue()
        self.result_queue: mp.Queue = mp.Queue()
        self.workers: List[mp.Process] = []
        self._submitted_count = 0

    def start(self) -> None:
        """Spawns worker processes."""
        self.workers = []
        for _ in range(self.num_workers):
            p = mp.Process(
                target=_worker_loop,
                args=(self.task_queue, self.result_queue, self.func)
            )
            p.daemon = True
            p.start()
            self.workers.append(p)

    def submit(self, item: Any) -> None:
        """Submits a single task item to the process queue."""
        self.task_queue.put(item)
        self._submitted_count += 1

    def submit_batch(self, items: List[Any]) -> None:
        """Submits multiple items to the process queue."""
        for item in items:
            self.submit(item)

    def collect_results(self) -> List[Tuple[Any, Any, Optional[str]]]:
        """Collects results, stops worker processes gracefully, and joins them."""
        results = []
        for _ in range(self._submitted_count):
            results.append(self.result_queue.get())

        # Send poison pills to stop workers
        for _ in range(self.num_workers):
            self.task_queue.put(None)

        for p in self.workers:
            p.join(timeout=2.0)

        self.workers = []
        self._submitted_count = 0
        return results
