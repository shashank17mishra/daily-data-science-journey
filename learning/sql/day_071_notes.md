# Day 071: SQL Case Statements & Conditional Logic

## Overview
Implement standard and advanced SQL conditional logic patterns using CASE expressions, COALESCE, NULLIF, and conditional aggregation in an SQLite environment.

## Objectives
- Understand practical application of SQL Case Statements & Conditional Logic.
- Write executable verification tests.

## Key Concepts
This exercise covers fundamental conditional logic features in SQL:
1. Searched `CASE` expressions: Categorizes values based on boolean predicate rules evaluated sequentially from top to bottom.
2. `COALESCE`: Returns the first non-NULL argument, enabling safe default value replacement for missing data or aggregate queries yielding NULL.
3. `NULLIF`: Compares two expressions and returns NULL if they are equal, avoiding runtime division-by-zero errors when calculating rates.
4. Conditional Aggregation: Combines aggregate functions (`SUM`, `COUNT`) with `CASE` logic to pivot tabular data and compute state counts across groups.
