# Day 015: Advanced Type Hinting and Generic Data Pipeline

## Overview
This exercise demonstrates intermediate to advanced Python type hinting features using the `typing` module. It implements a generic, type-safe data processing pipeline using `TypeVar`, `Generic`, `Protocol`, `Callable`, `Optional`, and structural subtyping.

## Objectives
- Understand how to use TypeVar and Generic to create reusable, type-safe data structures.
- Utilize Protocol for structural subtyping (duck typing with static type checks).
- Apply Callable, Union, and Optional type hints effectively in functional pipeline interfaces.
- Write robust pytest test suites verifying component behavior.

## Key Concepts
This exercise covers fundamental typing patterns in Python:

1. **`TypeVar` & `Generic`**: `T` and `R` allow `DataPipeline` to maintain strong type guarantees across generic input and output types without specifying concrete types upfront.
2. **`Protocol` & `@runtime_checkable`**: Implements structural subtyping (duck typing). `Serializable` defines expected methods without requiring class inheritance. `@runtime_checkable` allows standard `isinstance()` checks at runtime.
3. **`Callable`**: Annotates function arguments and attributes that receive callables with explicit argument and return types (`Callable[[T], T]`).
4. **`Optional` & `Union`**: Explicitly model values that can be `None` or accept one of multiple distinct types.
