# Day 074: SQL Views & Materialized Views

## Overview
Implementation of standard dynamic SQL Views and simulated Materialized Views in SQLite with change tracking, staleness detection, and manual refresh mechanisms.

## Objectives
- Understand practical application of SQL Views & Materialized Views.
- Write executable verification tests.

## Key Concepts
This exercise illustrates the core operational differences between standard SQL Views and Materialized Views:

1. **Standard SQL Views (`CREATE VIEW`)**:
   - Virtual tables computed dynamically every time they are queried.
   - Zero extra storage overhead.
   - Always reflect up-to-date data from underlying base tables instantly.
   - Query execution cost is paid on every SELECT request.

2. **Materialized Views (`CREATE MATERIALIZED VIEW`)**:
   - Physical tables that persist query results to disk/memory.
   - Fast query performance because pre-computed results are directly fetched without re-running joins or aggregations.
   - Can become **stale** when source tables are updated.
   - Requires periodic refresh mechanisms (`REFRESH MATERIALIZED VIEW` in PostgreSQL/Oracle, or custom application logic in SQLite/MySQL).

3. **Staleness Tracking Pattern**:
   - In systems without native materialized view support (like SQLite), materialized views can be implemented by storing metadata (`select_query`, `last_refreshed_at`) and logging modification timestamps on base tables (`last_modified_at`).
   - A view is marked stale when `max(last_modified_at) > last_refreshed_at`.
