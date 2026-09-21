"""Metaclasses and Dunder Methods in Python.

This module demonstrates advanced object-oriented programming techniques in Python,
including custom metaclasses, class attribute validation, namespace preparation,
descriptors, and object lifecycle dunder methods.
"""

from typing import Any, Dict, Type, Tuple, Optional


class Field:
    """Base descriptor for validated model attributes."""

    def __init__(self, required: bool = True, default: Any = None) -> None:
        self.required = required
        self.default = default
        self.name: Optional[str] = None
        self.private_name: Optional[str] = None

    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: Any, owner: Type[Any]) -> Any:
        if instance is None:
            return self
        if not hasattr(instance, self.private_name):
            if self.default is not None:
                setattr(instance, self.private_name, self.default)
            elif self.required:
                raise AttributeError(f"Attribute '{self.name}' has not been set.")
            else:
                return None
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: Any) -> None:
        self.validate(value)
        setattr(instance, self.private_name, value)

    def validate(self, value: Any) -> None:
        if value is None and self.required and self.default is None:
            raise ValueError(f"Field '{self.name}' cannot be None.")


class StringField(Field):
    """Descriptor for string type validation with length bounds."""

    def __init__(self, min_length: int = 0, max_length: Optional[int] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value: Any) -> None:
        super().validate(value)
        if value is None and not self.required:
            return
        if not isinstance(value, str):
            raise TypeError(f"Field '{self.name}' must be a str, got {type(value).__name__}.")
        if len(value) < self.min_length:
            raise ValueError(f"Field '{self.name}' must be at least {self.min_length} chars.")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f"Field '{self.name}' must be at most {self.max_length} chars.")


class IntegerField(Field):
    """Descriptor for integer type validation with range bounds."""

    def __init__(self, min_value: Optional[int] = None, max_value: Optional[int] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> None:
        super().validate(value)
        if value is None and not self.required:
            return
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"Field '{self.name}' must be an int, got {type(value).__name__}.")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Field '{self.name}' must be >= {self.min_value}.")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Field '{self.name}' must be <= {self.max_value}.")


class ModelMeta(type):
    """Metaclass that constructs dynamic models with auto-generated dunder methods.

    Features:
    - Tracks defined fields in order using __prepare__.
    - Registers defined model classes in a global model registry.
    - Automatically injects __repr__, __eq__, __len__, __getitem__, and __setitem__.
    """

    _registry: Dict[str, Type[Any]] = {}

    @classmethod
    def __prepare__(mcs, name: str, bases: Tuple[type, ...], **kwargs: Any) -> Dict[str, Any]:
        """Returns a dictionary to hold namespace attributes during class creation."""
        return {}

    def __new__(mcs, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any], **kwargs: Any) -> Any:
        fields: Dict[str, Field] = {}
        for key, value in list(namespace.items()):
            if isinstance(value, Field):
                fields[key] = value

        namespace["_fields"] = fields

        if "__repr__" not in namespace or namespace["__repr__"] is object.__repr__:
            def __repr__(self: Any) -> str:
                field_strs = []
                for fname in self._fields:
                    val = getattr(self, fname, None)
                    field_strs.append(f"{fname}={val!r}")
                return f"{self.__class__.__name__}({', '.join(field_strs)})"
            namespace["__repr__"] = __repr__

        if "__eq__" not in namespace or namespace["__eq__"] is object.__eq__:
            def __eq__(self: Any, other: Any) -> bool:
                if not isinstance(other, self.__class__):
                    return False
                return all(getattr(self, f, None) == getattr(other, f, None) for f in self._fields)
            namespace["__eq__"] = __eq__

        if "__len__" not in namespace:
            def __len__(self: Any) -> int:
                return len(self._fields)
            namespace["__len__"] = __len__

        if "__getitem__" not in namespace:
            def __getitem__(self: Any, item: str) -> Any:
                if item not in self._fields:
                    raise KeyError(f"Invalid field name: '{item}'")
                return getattr(self, item)
            namespace["__getitem__"] = __getitem__

        if "__setitem__" not in namespace:
            def __setitem__(self: Any, key: str, value: Any) -> None:
                if key not in self._fields:
                    raise KeyError(f"Invalid field name: '{key}'")
                setattr(self, key, value)
            namespace["__setitem__"] = __setitem__

        cls = super().__new__(mcs, name, bases, namespace)
        mcs._registry[name] = cls
        return cls

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Custom instantiation logic to accept kwargs matching field names."""
        instance = super().__call__()
        for fname, field in cls._fields.items():
            if fname in kwargs:
                setattr(instance, fname, kwargs[fname])
            elif field.default is not None:
                setattr(instance, fname, field.default)
            elif field.required and not hasattr(instance, field.private_name):
                raise ValueError(f"Missing required field '{fname}' during initialization.")
        return instance

    @classmethod
    def get_registered_models(mcs) -> Dict[str, Type[Any]]:
        """Returns a copy of registered models."""
        return dict(mcs._registry)


class BaseModel(metaclass=ModelMeta):
    """Base model class utilizing ModelMeta."""
    pass
