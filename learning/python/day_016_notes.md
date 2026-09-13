# Day 016: Dataclasses & Structured Data

## Overview
Learn how to use Python's dataclasses module to create clean, memory-efficient, and maintainable structured data classes with default values, post-initialization validation, immutability, and built-in serialization.

## Objectives
- Master core concepts of Dataclasses & Structured Data.
- Write clean, tested Python code.

## Key Concepts
Dataclasses (introduced in Python 3.7 via `dataclasses`) automate boilerplates like `__init__`, `__repr__`, and `__eq__`. Key features demonstrated include:
1. `@dataclass(frozen=True)` to create immutable structures suitable for hashing or reliable value objects.
2. `field(default_factory=...)` to avoid mutable default arguments (e.g., lists or dynamic UUIDs).
3. `__post_init__` hook for parameter verification and input normalization after `__init__` finishes.
4. `asdict` utility for converting nested structured data into plain dictionaries.
