# Day 020: CSV & Text Parsing

## Overview
Build a robust data parsing pipeline in Python using standard libraries (`csv`, `re`, `io`). Implement custom log text parsing with regex and sanitization, along with structured CSV data cleaning, schema validation, and CSV generation.

## Objectives
- Master core concepts of CSV & Text Parsing.
- Write clean, tested Python code.

## Key Concepts
This lesson covers text parsing and CSV processing in Python using standard libraries.

Key Concepts:
1. Regular Expressions (`re`): Named capture groups (`?P<name>...`) allow extracting specific fields from unstructured log strings.
2. In-Memory Strings (`io.StringIO`): Enables standard `csv.DictReader` and `csv.DictWriter` to operate on raw string data without reading/writing physical disk files.
3. Type Casting and Cleaning: Handling header whitespace, converting string primitives to target data types safely, and supplying default fallback values when parsing fails.
