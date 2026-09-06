"""
Day 006: File I/O, Context Managers, and CSV Processing using standard library.
"""
import csv
from pathlib import Path
from typing import List, Dict, Any

def write_data_to_csv(file_path: Path, data: List[Dict[str, Any]]) -> None:
    """Writes a list of dictionaries to a CSV file using csv.DictWriter."""
    if not data:
        raise ValueError("Cannot write empty dataset to CSV.")

    fieldnames = list(data[0].keys())
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def read_data_from_csv(file_path: Path) -> List[Dict[str, str]]:
    """Reads CSV file and returns list of record dicts."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
