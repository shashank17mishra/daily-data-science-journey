"""
Day 019: Custom JSON Parsing & Serialization

This module provides robust JSON serialization and deserialization capabilities
for complex Python data types including datetime, Decimal, UUID, set, and dataclasses.
"""

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Union
from uuid import UUID


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder handling complex data types."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return {"__type__": "datetime", "value": obj.isoformat()}
        if isinstance(obj, Decimal):
            return {"__type__": "decimal", "value": str(obj)}
        if isinstance(obj, UUID):
            return {"__type__": "uuid", "value": str(obj)}
        if isinstance(obj, set):
            return {"__type__": "set", "value": list(obj)}
        if is_dataclass(obj) and not isinstance(obj, type):
            return {"__type__": "dataclass", "class_name": obj.__class__.__name__, "value": asdict(obj)}
        return super().default(obj)


def custom_json_decoder(dct: dict[str, Any]) -> Any:
    """Decoder hook function to reconstruct custom types from JSON objects."""
    if "__type__" in dct:
        type_name = dct["__type__"]
        value = dct["value"]
        if type_name == "datetime":
            return datetime.fromisoformat(value)
        if type_name == "decimal":
            return Decimal(value)
        if type_name == "uuid":
            return UUID(value)
        if type_name == "set":
            return set(value)
        if type_name == "dataclass":
            return value
    return dct


def serialize_data(data: Any, indent: int = 2) -> str:
    """Serialize Python data structure into a JSON string."""
    return json.dumps(data, cls=CustomJSONEncoder, indent=indent)


def deserialize_data(json_str: str) -> Any:
    """Deserialize JSON string into Python data structure."""
    return json.loads(json_str, object_hook=custom_json_decoder)


def save_json(data: Any, filepath: Union[str, Path]) -> None:
    """Save Python data structure directly to a JSON file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, cls=CustomJSONEncoder, indent=2)


def load_json(filepath: Union[str, Path]) -> Any:
    """Load Python data structure directly from a JSON file."""
    path = Path(filepath)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f, object_hook=custom_json_decoder)
