from collections import deque, Counter
from itertools import groupby, islice
from functools import reduce, partial
from typing import Iterable, Iterator, Callable, TypeVar, Any, Dict, Tuple, NamedTuple, Union

T = TypeVar('T')
U = TypeVar('U')
Num = Union[int, float]

class Transaction(NamedTuple):
    transaction_id: str
    user_id: str
    amount: float
    category: str

def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Composes multiple single-argument functions from right to left.
    
    Example:
        compose(f, g)(x) is equivalent to f(g(x))
    """
    return reduce(lambda f, g: lambda x: f(g(x)), funcs, lambda x: x)

class StreamProcessor:
    """
    An advanced stream processing utility leveraging collections, itertools, and functools.
    Designed to process infinite or large data streams efficiently with minimal memory overhead.
    """

    @staticmethod
    def sliding_window_average(stream: Iterable[Num], window_size: int) -> Iterator[float]:
        """
        Computes a running sliding window average over a stream of numbers.
        Uses collections.deque for O(1) append/pop operations to maintain the window.
        """
        if window_size <= 0:
            raise ValueError("Window size must be greater than 0")
        
        window = deque(maxlen=window_size)
        current_sum = 0.0
        
        for val in stream:
            if len(window) == window_size:
                current_sum -= window[0]
            window.append(val)
            current_sum += val
            yield current_sum / len(window)

    @staticmethod
    def running_frequencies(stream: Iterable[T]) -> Iterator[Dict[T, int]]:
        """
        Tracks running frequencies of elements in a stream using collections.Counter.
        Yields a copy of the current frequency distribution at each step.
        """
        counter = Counter()
        for item in stream:
            counter[item] += 1
            yield dict(counter)

    @staticmethod
    def group_consecutive(stream: Iterable[T], key_func: Callable[[T], U]) -> Iterator[Tuple[U, list]]:
        """
        Groups consecutive elements in a stream by a key function using itertools.groupby.
        Yields tuples of (key, list of grouped items).
        """
        for key, group in groupby(stream, key=key_func):
            yield key, list(group)

    @staticmethod
    def batch_stream(stream: Iterable[T], batch_size: int) -> Iterator[list]:
        """
        Batches a stream into lists of a maximum size using itertools.islice.
        Memory-efficient and works on infinite generators.
        """
        if batch_size <= 0:
            raise ValueError("Batch size must be greater than 0")
        
        iterator = iter(stream)
        while True:
            batch = list(islice(iterator, batch_size))
            if not batch:
                break
            yield batch

# Practical pipeline helpers using functools.partial
filter_high_value_transactions = partial(filter, lambda tx: tx.amount >= 100.0)
filter_category = lambda cat: partial(filter, lambda tx: tx.category == cat)
