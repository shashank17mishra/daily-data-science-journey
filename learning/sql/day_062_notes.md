# Day 062: SQL DML: Insert, Update, Delete

## Overview
Implementation of a database repository demonstrating SQL Data Manipulation Language (DML) operations including INSERT, UPDATE, and DELETE statements with safe parameterized queries and transaction control.

## Objectives
- Understand practical application of SQL DML: Insert, Update, Delete.
- Write executable verification tests.

## Key Concepts
Data Manipulation Language (DML) consists of SQL statements used to manage and modify data within relational database tables.

Key Concepts Implemented:
1. **INSERT INTO**: Inserts new records into a database table. Supports single row inserts (`execute`) and batch/bulk inserts (`executemany`).
2. **UPDATE**: Modifies existing data. Can target single records by primary key or bulk updates based on conditional logic (e.g., category-wide price increases).
3. **DELETE FROM**: Removes specified rows from a table based on filtering criteria.
4. **Parameterized Queries**: Using `?` placeholders prevents SQL injection vulnerabilities by separating SQL statements from data arguments.
5. **Atomic Transactions**: Executing operations within connection context managers (`with conn:`) ensures auto-commit on success and rollback on failure.
