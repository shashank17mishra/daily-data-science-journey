import copy
import threading
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Type


class SingletonMeta(type):
    """Thread-safe Singleton metaclass."""

    _instances: Dict[Type[Any], Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DynamicFactory:
    """Dynamic Factory pattern allowing runtime creation registry."""

    def __init__(self) -> None:
        self._creators: Dict[str, Callable[..., Any]] = {}

    def register(self, key: str, creator: Callable[..., Any]) -> None:
        if key in self._creators:
            raise ValueError(f"Key '{key}' is already registered.")
        self._creators[key] = creator

    def unregister(self, key: str) -> None:
        if key not in self._creators:
            raise KeyError(f"Key '{key}' is not registered.")
        del self._creators[key]

    def create(self, key: str, *args: Any, **kwargs: Any) -> Any:
        if key not in self._creators:
            raise KeyError(f"Key '{key}' is not registered.")
        return self._creators[key](*args, **kwargs)


@dataclass(frozen=True)
class ModelConfig:
    """Immutable model configuration object constructed via builder."""

    model_type: str
    learning_rate: float
    epochs: int
    batch_size: int
    optimizer: str = "adam"


class ModelConfigBuilder:
    """Fluent builder with strict attribute validation for ModelConfig."""

    def __init__(self) -> None:
        self._model_type: Optional[str] = None
        self._learning_rate: Optional[float] = None
        self._epochs: Optional[int] = None
        self._batch_size: Optional[int] = None
        self._optimizer: str = "adam"

    def set_model_type(self, model_type: str) -> "ModelConfigBuilder":
        if not isinstance(model_type, str) or not model_type.strip():
            raise ValueError("model_type must be a non-empty string.")
        self._model_type = model_type
        return self

    def set_learning_rate(self, lr: float) -> "ModelConfigBuilder":
        if not isinstance(lr, (int, float)) or lr <= 0:
            raise ValueError("learning_rate must be a positive number.")
        self._learning_rate = float(lr)
        return self

    def set_epochs(self, epochs: int) -> "ModelConfigBuilder":
        if not isinstance(epochs, int) or epochs <= 0:
            raise ValueError("epochs must be a positive integer.")
        self._epochs = epochs
        return self

    def set_batch_size(self, batch_size: int) -> "ModelConfigBuilder":
        if not isinstance(batch_size, int) or batch_size <= 0:
            raise ValueError("batch_size must be a positive integer.")
        self._batch_size = batch_size
        return self

    def set_optimizer(self, optimizer: str) -> "ModelConfigBuilder":
        if not isinstance(optimizer, str) or not optimizer.strip():
            raise ValueError("optimizer must be a non-empty string.")
        self._optimizer = optimizer
        return self

    def build(self) -> ModelConfig:
        if self._model_type is None:
            raise ValueError("Missing required field: model_type")
        if self._learning_rate is None:
            raise ValueError("Missing required field: learning_rate")
        if self._epochs is None:
            raise ValueError("Missing required field: epochs")
        if self._batch_size is None:
            raise ValueError("Missing required field: batch_size")

        return ModelConfig(
            model_type=self._model_type,
            learning_rate=self._learning_rate,
            epochs=self._epochs,
            batch_size=self._batch_size,
            optimizer=self._optimizer,
        )


class PrototypeRegistry:
    """Prototype registry supporting object dynamic cloning and attribute override."""

    def __init__(self) -> None:
        self._prototypes: Dict[str, Any] = {}

    def register(self, prototype_id: str, prototype: Any) -> None:
        if prototype_id in self._prototypes:
            raise ValueError(f"Prototype with id '{prototype_id}' already registered.")
        self._prototypes[prototype_id] = prototype

    def unregister(self, prototype_id: str) -> None:
        if prototype_id not in self._prototypes:
            raise KeyError(f"Prototype with id '{prototype_id}' is not registered.")
        del self._prototypes[prototype_id]

    def clone(self, prototype_id: str, **attrs: Any) -> Any:
        if prototype_id not in self._prototypes:
            raise KeyError(f"Prototype with id '{prototype_id}' is not registered.")

        cloned_obj = copy.deepcopy(self._prototypes[prototype_id])
        for attr, value in attrs.items():
            if hasattr(cloned_obj, attr):
                setattr(cloned_obj, attr, value)
            elif isinstance(cloned_obj, dict) and attr in cloned_obj:
                cloned_obj[attr] = value
            else:
                raise AttributeError(f"Attribute '{attr}' does not exist on target prototype object.")
        return cloned_obj
