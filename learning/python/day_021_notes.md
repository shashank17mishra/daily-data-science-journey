# Day 021: Multithreading Basics

## Overview
Implement a thread-safe task processing pool using Python's threading module, queues, and locks to safely execute concurrent tasks and manage worker lifecycles.

## Objectives
- Understand threading fundamentals, synchronization, and the Python GIL.
- Use Threading Locks and Queues for safe state management and work distribution.
- Implement robust lifecycle management (start, submit, stop) for worker threads.

## Key Concepts
In Python, multithreading is useful for I/O-bound tasks (e.g., file operations, network requests). This exercise demonstrates fundamental concurrency concepts:
1. Thread-safe communication using `queue.Queue`, which internally handles locking when items are put or retrieved.
2. Synchronization using `threading.Lock` to prevent race conditions when appending to shared lists (`_results` and `_errors`).
3. Graceful worker shutdown using 'sentinel values' (poison pills like `None`) to signal worker threads to terminate cleanly after finishing queued tasks.
