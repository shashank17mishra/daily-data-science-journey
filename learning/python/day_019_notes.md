# Day 019: JSON Parsing & Serialization

## Overview
Learn intermediate JSON operations in Python including custom encoders, decoder object hooks, and handling complex non-standard data types like datetime, Decimal, UUID, sets, and dataclasses.

## Objectives
- Master core concepts of JSON Parsing & Serialization.
- Write clean, tested Python code.

## Key Concepts
This exercise demonstrates how to expand Python's standard `json` library capability using custom serialization subclasses and deserialization hooks.

Key Concepts Covered:
1. **Custom Encoding (`json.JSONEncoder`)**: Subclassing `json.JSONEncoder` to extend support for unsupported types like `datetime`, `Decimal`, `UUID`, `set`, and `dataclass` instances by appending type metadata (`__type__`).
2. **Custom Decoding (`object_hook`)**: Using the `object_hook` argument in `json.loads` or `json.load` to intercept JSON objects and reconstruct original Python objects based on type tags.
3. **File Utility Functions**: Wrapping JSON file operations (`save_json`, `load_json`) with path handling using `pathlib.Path`.
