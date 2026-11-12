# Day 073: SQL Set Operations: UNION, EXCEPT

## Overview
Demonstrates relational set operations in SQL (UNION, UNION ALL, EXCEPT, and INTERSECT) using SQLite. Covers deduplication, retention of duplicates, set difference, and set intersection for data reconciliation.

## Objectives
- Understand practical application of SQL Set Operations: UNION, EXCEPT.
- Write executable verification tests.

## Key Concepts
SQL Set Operations allow querying across multiple result sets produced by SELECT queries:

1. `UNION`: Merges distinct records from two query blocks, removing duplicates automatically. Requires column compatibility between SELECT statements.
2. `UNION ALL`: Merges all records from two query blocks without performing deduplication, making it computationally faster when duplicate elimination is not needed.
3. `EXCEPT` (or `MINUS` in Oracle): Computes relational difference (Set A \ Set B). It returns rows from the first query that are not present in the second query.
4. `INTERSECT`: Computes relational intersection (Set A ∩ Set B). It returns only rows common to both query results.

Requirements for Set Operations:
- Both queries must return the same number of columns.
- Corresponding columns must have compatible data types.
- `ORDER BY` applies to the final combined result set and should be placed at the very end of the statement.
