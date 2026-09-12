"""Data processing pipeline utilizing Python's typing module constructs."""

from typing import (
    TypeVar,
    Generic,
    Protocol,
    List,
    Dict,
    Callable,
    Optional,
    Union,
    Any,
    runtime_checkable,
)

T = TypeVar("T")
R = TypeVar("R")


@runtime_checkable
class Serializable(Protocol):
    """Protocol defining objects that can be serialized to a dictionary."""

    def to_dict(self) -> Dict[str, Any]:
        ...


class DataRecord:
    """Sample record implementing Serializable protocol."""

    def __init__(self, record_id: int, payload: str, score: float) -> None:
        self.record_id = record_id
        self.payload = payload
        self.score = score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "payload": self.payload,
            "score": self.score,
        }


class DataPipeline(Generic[T, R]):
    """Generic pipeline that transforms items of type T into items of type R."""

    def __init__(self) -> None:
        self._transformers: List[Callable[[T], T]] = []
        self._finalizer: Optional[Callable[[T], R]] = None

    def add_step(self, transformer: Callable[[T], T]) -> "DataPipeline[T, R]":
        """Registers an intermediate transformation step."""
        self._transformers.append(transformer)
        return self

    def set_finalizer(self, finalizer: Callable[[T], R]) -> None:
        """Sets the final transformation step producing output type R."""
        self._finalizer = finalizer

    def process_item(self, item: T) -> Union[R, T]:
        """Executes all pipeline steps on a single item."""
        current: T = item
        for step in self._transformers:
            current = step(current)
        
        if self._finalizer is not None:
            return self._finalizer(current)
        return current

    def process_batch(self, items: List[T]) -> List[Union[R, T]]:
        """Executes the pipeline over a batch of items."""
        return [self.process_item(item) for item in items]


def serialize_if_possible(item: Any) -> Union[Dict[str, Any], Any]:
    """Helper function that serializes an item if it adheres to Serializable protocol."""
    if isinstance(item, Serializable):
        return item.to_dict()
    return item
