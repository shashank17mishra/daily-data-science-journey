# Day 061: SQL DDL: Tables & Constraints

## Overview
Demonstrates SQL Data Definition Language (DDL) using SQLite in Python. Covers table creation, primary keys, foreign keys with referential actions, unique constraints, check constraints, and default values along with schema introspection.

## Objectives
- Understand practical application of SQL DDL: Tables & Constraints.
- Write executable verification tests.

## Key Concepts
SQL Data Definition Language (DDL) specifies database schema structure and constraints:

1. **PRIMARY KEY**: Uniquely identifies each record in a table and implicitly prevents NULL values.
2. **FOREIGN KEY**: Maintains referential integrity between child and parent tables (`employees.dept_id` references `departments.dept_id`). Note: SQLite requires explicit activation of foreign key constraints using `PRAGMA foreign_keys = ON;`.
3. **Referential Actions**: `ON DELETE RESTRICT` prevents deletion of parent records if child records exist.
4. **UNIQUE**: Guarantees distinct values in a column (`dept_name`, `email`).
5. **CHECK**: Enforces logical condition rules on values entered (`budget >= 0`, `salary > 0`).
6. **NOT NULL**: Disallows missing values.
7. **DEFAULT**: Sets initial standard values (e.g., `DATE('now')`).
