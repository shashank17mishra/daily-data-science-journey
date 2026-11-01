# Day 065: SQL Inner, Left, Right & Full Outer Joins

## Overview
Demonstrates relational database join operations (INNER JOIN, LEFT OUTER JOIN, RIGHT OUTER JOIN, and FULL OUTER JOIN) using Python's sqlite3 database engine, complete with compatibility fallbacks for engines lacking native RIGHT/FULL OUTER syntax.

## Objectives
- Understand practical application of SQL Inner, Left, Right & Full Outer Joins.
- Write executable verification tests.

## Key Concepts
SQL joins allow combining data across multiple relational tables based on key relationships:

1. **INNER JOIN**: Returns records that have matching values in both tables.
2. **LEFT (OUTER) JOIN**: Returns all records from the left table and matched records from the right table. Fields from the right table are NULL when no match exists.
3. **RIGHT (OUTER) JOIN**: Returns all records from the right table and matched records from the left table.
4. **FULL OUTER JOIN**: Returns all records when there is a match in either left or right table. Unmatched attributes on either side are NULL.

In SQLite, standard queries natively support INNER JOIN and LEFT JOIN. For compatibility across older SQLite versions, RIGHT JOIN can be emulated by swapping table order in a LEFT JOIN, and FULL OUTER JOIN can be emulated using `LEFT JOIN UNION ALL (RIGHT JOIN equivalent)`.
