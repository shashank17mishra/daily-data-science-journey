# Day 069: SQL Common Table Expressions (CTEs)

## Overview
Implement and verify SQL Common Table Expressions (CTEs) in Python using SQLite, covering non-recursive chained CTEs, recursive hierarchical queries, and window functions inside CTE blocks.

## Objectives
- Understand practical application of SQL Common Table Expressions (CTEs).
- Write executable verification tests.

## Key Concepts
Common Table Expressions (CTEs) are defined using the `WITH` clause and act as temporary, readable result sets accessible within an executing SQL query.

### Core Concepts Covered:
1. **Chained Non-Recursive CTEs (`WITH cte1 AS (...), cte2 AS (...)`)**: Allows modularizing complex queries into sequential transformation steps. In `get_department_sales_summary`, `dept_sales` aggregates sales per department, and `company_avg` calculates the overall average across departments using the first CTE as input.
2. **Recursive CTEs (`WITH RECURSIVE`)**: Essential for querying graph or tree structures like organizational hierarchies, bill-of-materials, or category trees. A recursive CTE consists of:
   - **Anchor Member**: Selects initial root record(s).
   - **UNION ALL**: Combines anchor and recursive results.
   - **Recursive Member**: Iteratively joins the CTE back to parent records until no more matching child records are returned.
3. **Window Functions within CTEs**: CTEs provide clean boundaries for computing window functions like `DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...)` and filtering their output in the outer `SELECT` query.
