import queue
import threading
from typing import Any, Callable, List, Tuple


class TaskProcessor:
    """Thread-safe task processor managing worker threads and queued tasks."""

    def __init__(self, num_workers: int = 4) -> None:
        if num_workers <= 0:
            raise ValueError("Number of workers must be at least 1.")
        self.num_workers = num_workers
        self.task_queue: queue.Queue = queue.Queue()
        self._results: List[Any] = []
        self._errors: List[Tuple[Any, Exception]] = []
        self._lock = threading.Lock()
        self._workers: List[threading.Thread] = []
        self._is_running = False

    def _worker_loop(self) -> None:
        while True:
            item = self.task_queue.get()
            if item is None:
                self.task_queue.task_done()
                break

            func, args, kwargs = item
            try:
                result = func(*args, **kwargs)
                with self._lock:
                    self._results.append(result)
            except Exception as exc:
                with self._lock:
                    self._errors.append((item, exc))
            finally:
                self.task_queue.task_done()

    def start(self) -> None:
        """Start worker threads."""
        if self._is_running:
            return
        self._is_running = True
        self._workers = []
        for i in range(self.num_workers):
            t = threading.Thread(target=self._worker_loop, name=f"Worker-{i+1}", daemon=True)
            t.start()
            self._workers.append(t)

    def submit(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        """Submit a task to be processed asynchronously by worker threads."""
        if not self._is_running:
            raise RuntimeError("TaskProcessor is not running. Call start() before submitting tasks.")
        self.task_queue.put((func, args, kwargs))

    def stop(self) -> None:
        """Gracefully wait for remaining tasks and stop worker threads."""
        if not self._is_running:
            return

        self.task_queue.join()
        for _ in range(self.num_workers):
            self.task_queue.put(None)

        for worker in self._workers:
            worker.join()

        self._is_running = False

    def get_results(self) -> List[Any]:
        """Thread-safe retrieval of task results."""
        with self._lock:
            return list(self._results)

    def get_errors(self) -> List[Tuple[Any, Exception]]:
        """Thread-safe retrieval of task execution errors."""
        with self._lock:
            return list(self._errors)
