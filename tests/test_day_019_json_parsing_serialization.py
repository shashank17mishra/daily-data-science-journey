"""
Unit tests for custom JSON serialization and parsing.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
import json
import pytest
from learning.python.day_019_json_parsing_serialization import (
    CustomJSONEncoder,
    deserialize_data,
    load_json,
    save_json,
    serialize_data,
)


@dataclass
class UserProfile:
    user_id: int
    username: str


def test_datetime_serialization():
    dt = datetime(2023, 10, 27, 12, 30, 45)
    serialized = serialize_data({"timestamp": dt})
    deserialized = deserialize_data(serialized)
    assert deserialized["timestamp"] == dt


def test_decimal_serialization():
    amount = Decimal("123.45")
    serialized = serialize_data({"price": amount})
    deserialized = deserialize_data(serialized)
    assert deserialized["price"] == amount
    assert isinstance(deserialized["price"], Decimal)


def test_uuid_serialization():
    unique_id = uuid4()
    serialized = serialize_data({"id": unique_id})
    deserialized = deserialize_data(serialized)
    assert deserialized["id"] == unique_id
    assert isinstance(deserialized["id"], UUID)


def test_set_serialization():
    tags = {"python", "json", "testing"}
    serialized = serialize_data({"tags": tags})
    deserialized = deserialize_data(serialized)
    assert deserialized["tags"] == tags
    assert isinstance(deserialized["tags"], set)


def test_dataclass_serialization():
    profile = UserProfile(user_id=42, username="alice")
    serialized = serialize_data({"profile": profile})
    deserialized = deserialize_data(serialized)
    assert deserialized["profile"] == {"user_id": 42, "username": "alice"}


def test_file_io(tmp_path):
    test_file = tmp_path / "test_data.json"
    data = {
        "id": UUID("12345678-1234-5678-1234-567812345678"),
        "created_at": datetime(2023, 1, 1, 0, 0, 0),
        "balance": Decimal("999.99"),
        "roles": {"admin", "user"},
    }

    save_json(data, test_file)
    assert test_file.exists()

    loaded = load_json(test_file)
    assert loaded == data


def test_unsupported_type_raises():
    class Unserializable:
        pass

    with pytest.raises(TypeError):
        serialize_data({"item": Unserializable()})
