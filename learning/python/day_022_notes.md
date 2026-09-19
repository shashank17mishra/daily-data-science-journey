# Day 022: Multiprocessing Basics

## Overview
Implementation of parallel task processing using Python's multiprocessing module, featuring multiprocessing.Pool, Process, Queue, and graceful termination patterns.

## Objectives
- Master core concepts of Multiprocessing Basics.
- Write clean, tested Python code.

## Key Concepts
### Multiprocessing in Python

Python's `multiprocessing` module bypasses the Global Interpreter Lock (GIL) by spawning separate operating system processes, each with its own Python interpreter and memory space. This enables full utilization of multi-core CPUs for CPU-bound tasks.

#### Key Components Demonstrated:
1. **High-Level Abstraction (`multiprocessing.Pool`)**:
   `run_parallel_map` leverages `Pool.map` to divide a sequence of inputs across worker processes automatically.

2. **Low-Level Process & IPC (`Process` and `Queue`)**:
   `QueueProcessPipeline` creates individual `mp.Process` instances and connects them via thread/process-safe FIFO `mp.Queue` channels.

3. **Poison Pill Pattern**:
   Workers run in an infinite `while True` loop listening for tasks. Sending `None` (a sentinel value or 'poison pill') signals workers to gracefully exit their execution loop.

4. **Serialization Requirement**:
   Functions and data passed across process boundaries must be pickleable, which is why top-level functions are used.
