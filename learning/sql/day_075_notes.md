# Day 075: SQL Schema Normalization (1NF to 3NF)

## Overview
Learn and execute relational database schema normalization from Unnormalized Form (UNF) to First Normal Form (1NF), Second Normal Form (2NF), and Third Normal Form (3NF) using Python's SQLite engine.

## Objectives
- Understand practical application of SQL Schema Normalization (1NF to 3NF).
- Identify and eliminate repeating groups, partial key dependencies, and transitive dependencies.
- Verify database normalization properties such as lossless join decomposition and referential integrity using unit tests.

## Key Concepts
Database schema normalization is a systematic approach of decomposing tables to eliminate data redundancy, prevent update/insertion/deletion anomalies, and ensure functional dependencies are correctly structured.

1. **Unnormalized Form (UNF)**: Contains repeating groups or composite/multi-valued attributes (e.g., delimited CSV strings storing items inside an order table row).
2. **First Normal Form (1NF)**: Requires atomic values (no repeating groups/lists in a cell) and a designated primary key.
3. **Second Normal Form (2NF)**: Meets 1NF requirements and eliminates partial dependencies—every non-key attribute must functionally depend on the *entire* primary key. In a composite key `(order_id, item_id)`, `item_name` depends only on `item_id`, so it is separated into an `items` table.
4. **Third Normal Form (3NF)**: Meets 2NF requirements and eliminates transitive dependencies—non-key attributes must not depend on other non-key attributes. For instance, `customer_id -> customer_zip -> city, state` contains a transitive dependency where `city` depends on `customer_zip`. Decomposing this into `zip_locations`, `customers`, and `orders` tables achieves 3NF.
