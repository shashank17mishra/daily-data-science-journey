# Day 030: Unit Testing with pytest

## Overview
An advanced implementation of a thread-safe Token Bucket Rate Limiter designed for testability using dependency injection. The accompanying pytest suite demonstrates advanced testing patterns including deterministic time mocking, parameterized testing, exception validation, and fixture composition.

## Objectives
- Design highly testable code using dependency injection for time-dependent logic.
- Write robust, deterministic unit tests without relying on fragile time.sleep calls.
- Leverage pytest fixtures, parameterization, and exception assertions for comprehensive coverage.

## Key Concepts
This exercise demonstrates advanced unit testing patterns in Python using pytest. By implementing a Token Bucket Rate Limiter, we encounter a common testing challenge: dealing with time-dependent logic. Instead of using fragile `time.sleep()` calls which slow down test suites and introduce non-determinism, we use Dependency Injection. By passing a custom `time_func` (defaulting to `time.time`), we can inject a `MockClock` in our tests. This allows us to manually and instantly advance time (`mock_clock.tick()`), ensuring tests are 100% deterministic, lightning-fast, and robust. The test suite also demonstrates pytest fixtures, parameterized testing to run multiple test cases through a single test function, and strict exception verification using `pytest.raises`.
