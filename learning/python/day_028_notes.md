# Day 028: Collections, Itertools & Functools

## Overview
An advanced stream processing engine that demonstrates the powerful synergy of Python's collections, itertools, and functools modules. It implements sliding windows, running frequency analysis, consecutive grouping, and stream batching with functional composition.

## Objectives
- Master core concepts of Collections, Itertools & Functools.
- Write clean, tested Python code.
- Implement memory-efficient stream processing using generators.
- Leverage functional composition and partial application for clean pipeline design.

## Key Concepts
This exercise demonstrates how to build high-performance, memory-efficient data pipelines using Python's standard library modules: `collections`, `itertools`, and `functools`.

1. **collections.deque**: Used to implement a sliding window average. Deques have O(1) appends and pops from both ends, making them significantly faster than standard lists for sliding window operations.
2. **collections.Counter**: Used to track running frequencies of streaming items. It provides an elegant and fast way to maintain multiset tallies.
3. **itertools.groupby**: Groups consecutive elements matching a key function. It processes data lazily, which is ideal for streaming data.
4. **itertools.islice**: Used to slice an iterator without consuming the entire stream into memory, allowing us to batch streams of arbitrary size.
5. **functools.reduce & partial**: Used to build a functional composition pipeline (`compose`) and pre-configure filtering functions (`partial`), demonstrating clean, reusable functional programming patterns in Python.
