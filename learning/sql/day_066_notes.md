# Day 066: SQL Subqueries & Correlated Queries

## Overview
Practical implementation of standard SQL subqueries and correlated queries using SQLite in Python. Demonstrates non-correlated scalar subqueries, correlated WHERE filtering, correlated SELECT attributes, and EXISTS/NOT EXISTS filtering.

## Objectives
- Understand practical application of SQL Subqueries & Correlated Queries.
- Write executable verification tests.

## Key Concepts
SQL Subqueries are nested query blocks within a primary query:

1. Non-Correlated Subquery:
- Executes independently of the outer query.
- Evaluated once before the outer query runs.
- Example: `WHERE salary > (SELECT AVG(salary) FROM employees)`.

2. Correlated Subquery:
- References columns from the outer query alias (e.g., `WHERE e2.department_id = e1.department_id`).
- Re-evaluated dynamically for each row processed by the outer query.
- Can appear in the `WHERE` clause (filtering), `SELECT` clause (computing derived fields per row), or with operators like `EXISTS` and `NOT EXISTS` (efficient set existence checks).
