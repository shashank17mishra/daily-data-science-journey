# Day 070: SQL Indexing & Query Optimization

## Overview
Implement and verify SQL query optimization techniques using SQLite indexing, query plan analysis with EXPLAIN QUERY PLAN, and performance measurement.

## Objectives
- Understand practical application of SQL Indexing & Query Optimization.
- Write executable verification tests.

## Key Concepts
This exercise covers SQL indexing and query optimization fundamentals using standard SQLite:
1. Query Execution Plans: Using `EXPLAIN QUERY PLAN` to inspect database search algorithms (Full Table Scan `SCAN TABLE` vs Binary B-Tree Search `SEARCH TABLE USING INDEX`).
2. Single & Composite Indexing: Demonstrates creating single column indexes and multi-column composite indexes tailored to `WHERE` filter clauses.
3. Result Correctness & Performance Measurement: Verifies that creating indexes optimizes query paths without altering dataset output or query correctness.
