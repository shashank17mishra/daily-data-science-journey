# Day 026: Custom Context Managers

## Overview
An advanced exploration of Python's context management protocol. This exercise implements a robust, class-based transactional state manager with nested transaction support and exception handling, alongside a generator-based environment variable override manager.

## Objectives
- Master the context management protocol using __enter__ and __exit__.
- Implement nested transaction rollbacks and state snapshotting.
- Utilize contextlib.contextmanager for elegant, generator-based resource management.
- Handle and selectively suppress exceptions within custom context managers.

## Key Concepts
This exercise covers two primary ways of implementing custom context managers in Python:

1. **Class-Based Context Managers (`__enter__` / `__exit__`)**:
   - The `Transaction` class manages state modifications on a `TransactionalStore` object.
   - `__enter__` takes a deep copy snapshot of the store's data and pushes it onto a transaction stack.
   - `__exit__` handles cleanups and exceptions. If an exception occurs, it restores the state from the snapshot. If the exception type matches the `suppress_exceptions` tuple, returning `True` prevents the exception from propagating up the call stack.
   - This stack-based approach naturally supports nested transactions.

2. **Generator-Based Context Managers (`@contextmanager`)**:
   - The `temp_env_vars` utility uses `contextlib.contextmanager` to temporarily override environment variables.
   - It saves the original environment state, yields control to the block using `yield`, and uses a `finally` block to guarantee that the original environment is restored even if an exception is raised inside the context block.
