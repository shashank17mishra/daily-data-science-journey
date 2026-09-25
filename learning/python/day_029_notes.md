# Day 29: Logging Architecture & Formatters

## Overview
An advanced exploration of Python's logging architecture. This exercise implements a custom structured JSON formatter, a dynamic thread-local context filter, and an in-memory ring buffer handler to demonstrate custom log routing, formatting, and filtering.

## Objectives
- Understand the flow of LogRecords through Loggers, Filters, Handlers, and Formatters.
- Implement a custom JSON Formatter that handles standard fields, dynamic extra attributes, and exceptions.
- Create a thread-safe Context Filter to inject request-scoped metadata into logs.
- Build a custom Memory Ring Buffer Handler to retain only the most recent N log records in memory.

## Key Concepts
This exercise demonstrates the complete Python logging pipeline: Loggers, Filters, Handlers, and Formatters. 

1. `StructuredJSONFormatter` inherits from `logging.Formatter` and overrides `format()`. It extracts standard fields, dynamically collects any custom attributes attached to the `LogRecord` (excluding standard fields), formats exceptions cleanly, and serializes the output to a single-line JSON string.
2. `ContextFilter` uses thread-local storage (`threading.local`) to dynamically inject contextual metadata (like request IDs) into every log record processed by the logger. This is crucial for tracing requests in multi-threaded or concurrent environments.
3. `MemoryRingBufferHandler` is a custom handler that uses a thread-safe `collections.deque` with a fixed capacity to keep only the most recent N log records in memory. This is highly useful for diagnostics, allowing applications to dump recent debug logs only when an error occurs.
