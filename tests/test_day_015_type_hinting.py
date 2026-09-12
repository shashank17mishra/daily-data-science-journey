"""Tests for Day 015: Type Hinting and Typing Module."""

import pytest
from learning.python.day_015_type_hinting import (
    Serializable,
    DataRecord,
    DataPipeline,
    serialize_if_possible,
)


def test_serializable_protocol() -> None:
    record = DataRecord(1, "test_payload", 95.5)
    assert isinstance(record, Serializable)
    assert record.to_dict() == {
        "record_id": 1,
        "payload": "test_payload",
        "score": 95.5,
    }


def test_data_pipeline_transformations() -> None:
    pipeline: DataPipeline[int, str] = DataPipeline()
    pipeline.add_step(lambda x: x * 2).add_step(lambda x: x + 5)
    pipeline.set_finalizer(lambda x: f"Result: {x}")

    result = pipeline.process_item(10)
    assert result == "Result: 25"


def test_data_pipeline_without_finalizer() -> None:
    pipeline: DataPipeline[str, str] = DataPipeline()
    pipeline.add_step(lambda s: s.strip()).add_step(lambda s: s.upper())

    result = pipeline.process_item("  hello world  ")
    assert result == "HELLO WORLD"


def test_data_pipeline_batch_processing() -> None:
    pipeline: DataPipeline[int, int] = DataPipeline()
    pipeline.add_step(lambda x: x ** 2)
    
    results = pipeline.process_batch([1, 2, 3, 4])
    assert results == [1, 4, 9, 16]


def test_serialize_if_possible() -> None:
    record = DataRecord(42, "data", 10.0)
    raw_dict = serialize_if_possible(record)
    assert isinstance(raw_dict, dict)
    assert raw_dict["record_id"] == 42

    non_serializable = "just a string"
    assert serialize_if_possible(non_serializable) == "just a string"
