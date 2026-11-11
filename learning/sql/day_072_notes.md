# Day 072: SQL Date & String Utilities

## Overview
Implement intermediate SQL queries using SQLite string manipulation functions (SUBSTR, INSTR, TRIM, LOWER, UPPER, PRINTF) and date/time functions (STRFTIME, JULIANDAY) to clean raw analytical data, calculate user tenure, format IDs, and aggregate monthly activity.

## Objectives
- Understand practical application of SQL Date & String Utilities.
- Write executable verification tests.

## Key Concepts
This exercise demonstrates intermediate SQL String and Date utilities within SQLite.

Key Concepts:
1. String Parsing: `INSTR(email, '@')` finds the delimiter position, while `SUBSTR(email, pos + 1)` extracts the domain suffix. `LOWER(...)` ensures case insensitivity.
2. Casing & Normalization: Common Table Expressions (CTEs) split messy strings. `TRIM` removes padding whitespace, `UPPER` formats last names, and title-casing is achieved via string concatenation (`UPPER(SUBSTR(..., 1, 1)) || LOWER(SUBSTR(..., 2))`).
3. Zero-Padding Formats: `PRINTF('USR-%04d', user_id)` creates consistent formatted identifier strings.
4. Date Functions & Arithmetic: `JULIANDAY` computes epoch Julian days to perform date differences (`JULIANDAY(date2) - JULIANDAY(date1)`). `STRFTIME('%Y-%m', date)` truncates timestamps into year-month buckets for temporal aggregation.
