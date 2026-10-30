# Day 063: SQL Filtering, Sorting & Limiting

## Overview
Demonstrates relational database operations for filtering, sorting, and paginating query results using Python's standard `sqlite3` module. Encapsulates query building inside a reusable repository pattern to avoid common SQLite in-memory scope pitfalls.

## Objectives
- Understand practical application of SQL Filtering, Sorting & Limiting.
- Write executable verification tests.

## Key Concepts
This exercise addresses a critical pitfall when working with SQLite in Python testing environments: SQLite in-memory databases (`:memory:`) create a distinct, isolated database connection each time `sqlite3.connect(':memory:')` is invoked. In the previous implementation attempt, separate function calls established new database instances, leading to `no such table: products` errors.

To resolve this permanently:
1. The operations are encapsulated inside a `ProductRepository` class that maintains a persistent `sqlite3.Connection` instance throughout its lifecycle.
2. SQL filtering parameters use parameter binding (`?` placeholders) to prevent SQL injection vulnerabilities.
3. Dynamic column and sorting direction specifications are validated against an explicit whitelist of allowed schema columns before dynamic query composition.
4. Pagination techniques combine `LIMIT` and `OFFSET` clauses for reliable results browsing.
