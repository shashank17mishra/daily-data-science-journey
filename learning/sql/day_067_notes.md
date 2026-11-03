# Day 067: SQL Window Functions: ROW_NUMBER, RANK

## Overview
Demonstrates SQL Window Functions (ROW_NUMBER, RANK, DENSE_RANK) using SQLite in Python. Illustrates partitioning, ordering, tie-handling, and filtering top N items per group.

## Objectives
- Understand practical application of SQL Window Functions: ROW_NUMBER, RANK.
- Write executable verification tests.

## Key Concepts
SQL Window Functions allow calculations across sets of rows related to the current row without collapsing the rows like standard GROUP BY queries do.

Key Window Functions for Ranking:
1. ROW_NUMBER(): Assigns a unique sequential integer to each row within a partition, starting at 1. Tied values receive arbitrary consecutive row numbers.
2. RANK(): Assigns ranks with gaps. Tied values share the same rank, and the next rank skips numbers according to the count of ties (e.g., 1, 2, 2, 4).
3. DENSE_RANK(): Assigns ranks without gaps. Tied values share the same rank, and the next rank is incremented by 1 (e.g., 1, 2, 2, 3).

Common Pattern: Top N Per Group
Window functions cannot be directly used inside a WHERE clause because windowing operates after WHERE filtering. CTEs (Common Table Expressions via `WITH`) or subqueries are used to construct ranks first, followed by filtering `WHERE rank_val <= N`.
