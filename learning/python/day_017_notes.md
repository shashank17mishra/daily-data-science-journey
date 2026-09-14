# Day 017: String Formatting & Regex Basics

## Overview
Learn how to parse structured log data using Python's `re` module with named capture groups, format log summaries using advanced f-string format specifiers, and sanitize sensitive information like IP and email addresses.

## Objectives
- Master core concepts of String Formatting & Regex Basics.
- Write clean, tested Python code.

## Key Concepts
This exercise covers pattern extraction and text formatting in Python:

1. **Named Capture Groups (`?P<name>...`)**: Used in regular expressions to extract domain-specific entities (like timestamps, log levels, usernames) directly into named key-value mappings using `match.groupdict()`.
2. **Regex Subbing (`re.sub`)**: Used for text sanitization and data masking (e.g., stripping out PII like emails and IP addresses).
3. **F-String Formatting Specifiers**: Explores advanced string formatting options:
   - Padding & Zero-filling: `:03d` pads numbers with leading zeros up to 3 digits.
   - Alignment: `<` left-aligns text, `>` right-aligns text, and `^` centers text within a specified width field.
