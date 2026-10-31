# Day 064: SQL Aggregations & Group By

## Overview
Demonstrates relational database aggregations using SQLite. Covers core aggregate functions (COUNT, SUM, AVG, MIN, MAX), single and multi-column GROUP BY clauses, group filtering with HAVING, and conditional aggregations using CASE WHEN expressions.

## Objectives
- Understand practical application of SQL Aggregations & Group By.
- Write executable verification tests.

## Key Concepts
This exercise demonstrates key SQL aggregation techniques:
1. Core Aggregations: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` evaluate values across grouped rows.
2. `GROUP BY`: Groups output rows sharing identical column values.
3. `HAVING` vs `WHERE`: `WHERE` filters rows before grouping, while `HAVING` filters group summaries after aggregation.
4. Conditional Aggregation: Combining `SUM` or `COUNT` with `CASE WHEN` enables pivot-table behavior within standard SQL.
