"""
Day 017: String Formatting & Regex Basics

This module demonstrates parsing, sanitizing, and formatting unstructured string
data (e.g., system log entries) using Python's standard `re` library and f-strings.
"""

import re
from typing import Dict, Any, Optional

# Regex pattern with named capture groups for parsing standard log entries
LOG_PATTERN = re.compile(
    r"^\[(?P<timestamp>[^\]]+)\]\s+"
    r"(?P<level>INFO|WARNING|ERROR|DEBUG)\s+"
    r"\[(?P<user>[^\]]+)\]\s+"
    r"(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+-\s+"
    r"(?P<message>.*)$"
)

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
IP_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def parse_log_entry(log_line: str) -> Optional[Dict[str, str]]:
    """
    Parses a log line using named regex groups.

    Args:
        log_line: Log string in the format '[TIMESTAMP] LEVEL [USER] IP - MESSAGE'

    Returns:
        A dictionary of captured log attributes, or None if the pattern does not match.
    """
    match = LOG_PATTERN.match(log_line.strip())
    if not match:
        return None
    return match.groupdict()


def sanitize_log_message(text: str) -> str:
    """
    Redacts email addresses and IP addresses from a text string.

    Args:
        text: Input string potentially containing sensitive information.

    Returns:
        Sanitized text with masked emails and IPs.
    """
    # Replace emails with [REDACTED_EMAIL]
    sanitized = EMAIL_REGEX.sub("[REDACTED_EMAIL]", text)
    # Replace IP addresses with [REDACTED_IP]
    sanitized = IP_REGEX.sub("[REDACTED_IP]", sanitized)
    return sanitized


def format_log_summary(log_data: Dict[str, Any], line_number: int = 1) -> str:
    """
    Formats log data into a standardized summary line using f-string specifiers.

    Args:
        log_data: Dictionary containing parsed log keys (timestamp, level, user, ip, message)
        line_number: Line count indicator for alignment formatting

    Returns:
        Formatted summary string with alignment and padding.
    """
    level = log_data.get("level", "UNKNOWN").upper()
    user = log_data.get("user", "N/A")
    msg = log_data.get("message", "").strip()

    # Alignment specifiers: line_number right-aligned (3 width, zero padded),
    # level left-aligned (7 width), user centered (12 width)
    return f"#{line_number:03d} | [{level:<7s}] | User: {user:^12s} | Content: {msg}"
