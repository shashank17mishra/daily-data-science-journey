# Day 023: Asyncio & Async/Await

## Overview
Implementation of an asynchronous task pool with rate limiting using asyncio.Semaphore and resilient retry execution with exponential backoff.

## Objectives
- Master core concepts of Asyncio & Async/Await.
- Write clean, tested Python code.

## Key Concepts
Python's `asyncio` module provides single-threaded concurrent execution using coroutines, an event loop, and non-blocking I/O primitives. Key concepts implemented in this task include:

1. **Coroutines & `async`/`await`**: Declaring asynchronous functions with `async def` and yielding control back to the event loop using `await` during I/O operations.
2. **Concurrency Control via `asyncio.Semaphore`**: Prevents overwhelming external services or exceeding resource limits by bounding the maximum number of simultaneous coroutine executions.
3. **Batch Gathering via `asyncio.gather`**: Concurrently runs multiple tasks and collects their return values in order.
4. **Async Retry Mechanism**: Handles transient failures gracefully with exponential backoff without blocking the underlying thread.
