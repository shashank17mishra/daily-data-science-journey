"""Unit tests for CSV and Text Parsing pipeline."""

import pytest
from learning.python.day_020_csv_text_parsing import (
    parse_log_line,
    clean_csv_stream,
    export_to_csv,
)


def test_parse_log_line_valid_with_metadata():
    line = "[2026-03-30 10:00:00] ERROR Database connection failed | retry=3 host=db01"
    parsed = parse_log_line(line)
    assert parsed is not None
    assert parsed["timestamp"] == "2026-03-30 10:00:00"
    assert parsed["level"] == "ERROR"
    assert parsed["message"] == "Database connection failed"
    assert parsed["metadata"] == {"retry": "3", "host": "db01"}


def test_parse_log_line_valid_without_metadata():
    line = "[2026-03-30 10:05:00] INFO Service started"
    parsed = parse_log_line(line)
    assert parsed is not None
    assert parsed["level"] == "INFO"
    assert parsed["metadata"] == {}


def test_parse_log_line_invalid():
    assert parse_log_line("Invalid log format string") is None
    assert parse_log_line("") is None


def test_clean_csv_stream_basic():
    csv_data = " name , age , city \n Alice , 30 , NY \n Bob , 25 , LA "
    records = clean_csv_stream(csv_data)
    assert len(records) == 2
    assert records[0] == {"name": "Alice", "age": "30", "city": "NY"}
    assert records[1] == {"name": "Bob", "age": "25", "city": "LA"}


def test_clean_csv_stream_with_schema_and_defaults():
    csv_data = "id,score,active\n1,95.5,True\n2,,False\n3,invalid,True"
    schema = {"id": int, "score": float}
    defaults = {"score": 0.0}

    records = clean_csv_stream(csv_data, schema=schema, default_values=defaults)
    assert len(records) == 3
    assert records[0]["id"] == 1
    assert records[0]["score"] == 95.5
    assert records[1]["score"] == 0.0
    assert records[2]["score"] == 0.0


def test_clean_csv_stream_empty():
    assert clean_csv_stream("") == []


def test_export_to_csv():
    records = [
        {"name": "Alice", "age": 30, "role": "Admin"},
        {"name": "Bob", "age": 25, "role": "User"}
    ]
    fieldnames = ["name", "role"]
    expected = "name,role\nAlice,Admin\nBob,User\n"
    output = export_to_csv(records, fieldnames)
    assert output == expected
