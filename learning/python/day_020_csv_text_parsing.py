"""Day 020: CSV & Text Parsing Pipeline.

This module provides utilities to parse semi-structured log text,
clean and validate standard CSV streams, and format parsed data back
into structured CSV format.
"""

import csv
import io
import re
from typing import Any, Dict, List, Optional


LOG_PATTERN = re.compile(
    r"^\[(?P<timestamp>[^\]]+)\]\s+"
    r"(?P<level>INFO|WARNING|ERROR|DEBUG)\s+"
    r"(?P<message>.*?)"
    r"(?:\s+\|\s+(?P<metadata>.*))?$"
)


def parse_log_line(line: str) -> Optional[Dict[str, Any]]:
    """Parse a single log line into a structured dictionary.

    Expected format: [TIMESTAMP] LEVEL Message | key1=val1 key2=val2
    """
    line = line.strip()
    if not line:
        return None

    match = LOG_PATTERN.match(line)
    if not match:
        return None

    data = match.groupdict()
    metadata_raw = data.pop("metadata", None)
    metadata = {}

    if metadata_raw:
        kv_pairs = metadata_raw.split()
        for pair in kv_pairs:
            if "=" in pair:
                k, v = pair.split("=", 1)
                metadata[k] = v

    data["metadata"] = metadata
    return data


def clean_csv_stream(
    csv_content: str,
    schema: Optional[Dict[str, type]] = None,
    default_values: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """Parse and clean CSV data from a string content.

    - Strips whitespace from headers and values.
    - Casts values according to optional schema.
    - Applies default values for missing or empty fields.
    """
    if not csv_content.strip():
        return []

    reader = csv.DictReader(io.StringIO(csv_content.strip()))
    cleaned_records = []
    schema = schema or {}
    default_values = default_values or {}

    for row in reader:
        cleaned_row = {}
        for key, value in row.items():
            if key is None:
                continue
            clean_key = key.strip()
            clean_val = value.strip() if value is not None else ""

            if clean_val == "" and clean_key in default_values:
                clean_val = default_values[clean_key]
            elif clean_val != "" and clean_key in schema:
                try:
                    target_type = schema[clean_key]
                    clean_val = target_type(clean_val)
                except (ValueError, TypeError):
                    clean_val = default_values.get(clean_key, clean_val)

            cleaned_row[clean_key] = clean_val
        cleaned_records.append(cleaned_row)

    return cleaned_records


def export_to_csv(records: List[Dict[str, Any]], fieldnames: List[str]) -> str:
    """Serialize a list of dictionaries into a CSV formatted string."""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()

    for record in records:
        filtered_record = {k: record.get(k, "") for k in fieldnames}
        writer.writerow(filtered_record)

    return output.getvalue()
