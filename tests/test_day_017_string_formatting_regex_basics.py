"""
Unit tests for Day 017: String Formatting & Regex Basics
"""

import pytest
from learning.python.day_017_string_formatting_regex_basics import (
    parse_log_entry,
    sanitize_log_message,
    format_log_summary,
)


def test_parse_log_entry_valid():
    raw_log = "[2023-10-27 10:15:30] ERROR [admin] 192.168.1.50 - Failed login attempt"
    parsed = parse_log_entry(raw_log)
    
    assert parsed is not None
    assert parsed["timestamp"] == "2023-10-27 10:15:30"
    assert parsed["level"] == "ERROR"
    assert parsed["user"] == "admin"
    assert parsed["ip"] == "192.168.1.50"
    assert parsed["message"] == "Failed login attempt"


def test_parse_log_entry_invalid():
    invalid_log = "INVALID LOG FORMAT DATA"
    parsed = parse_log_entry(invalid_log)
    assert parsed is None


def test_sanitize_log_message():
    raw_message = "Contact john.doe@example.com at IP 10.0.0.1 for support."
    sanitized = sanitize_log_message(raw_message)
    
    assert "john.doe@example.com" not in sanitized
    assert "10.0.0.1" not in sanitized
    assert sanitized == "Contact [REDACTED_EMAIL] at IP [REDACTED_IP] for support."


def test_format_log_summary():
    log_data = {
        "level": "INFO",
        "user": "alice",
        "message": "User session started",
    }
    summary = format_log_summary(log_data, line_number=5)
    
    # Verify padding and alignment
    assert summary == "#005 | [INFO   ] | User:    alice     | Content: User session started"
