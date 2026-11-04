# Day 068: SQL Window Functions: LAG, LEAD, SUM OVER

## Overview
Learn and apply core SQL window functions (LAG, LEAD, and SUM OVER) to perform partition-based analytics, time-series calculations, and cumulative totals in Python with SQLite.

## Objectives
- Understand practical application of SQL Window Functions: LAG, LEAD, SUM OVER.
- Write executable verification tests.

## Key Concepts
SQL Window Functions perform calculations across a set of table rows related to the current row without collapsing rows like standard aggregate functions do.

1. `LAG(column, offset, default)`: Accesses data from a previous row within the partition. Ideal for computing day-over-day or period-over-period differences.
2. `LEAD(column, offset, default)`: Accesses data from a future row within the partition. Useful for predictive metrics or next-event analysis.
3. `SUM(column) OVER (PARTITION BY ... ORDER BY ...)`: Computes cumulative running totals for sequential rows within each partition context.
