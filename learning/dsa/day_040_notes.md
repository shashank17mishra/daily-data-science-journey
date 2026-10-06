# Day 040: Singly Linked List Operations

## Overview
Implementation of a standard Singly Linked List data structure in Python, featuring key pointer manipulation operations such as appending, prepending, arbitrary insertion, deletion by value/index, linear search, and in-place reversal.

## Objectives
- Understand algorithmic mechanics of Singly Linked List Operations.
- Implement unit tests for edge cases.

## Key Concepts
This module provides a pure-Python implementation of a Singly Linked List (`SinglyLinkedList`) and node structure (`Node`). Key operations implemented include:
- **`append` / `prepend`**: Time complexity O(N) for append (without a tail pointer) and O(1) for prepend.
- **`insert_at` / `delete_at`**: Positional updates with O(N) time complexity and strict boundary checking.
- **`delete_value`**: Linear search and pointer updates to bypass and remove target nodes.
- **`reverse`**: In-place reversal in O(N) time and O(1) space complexity by tracking three pointers (`prev`, `current`, `next_node`).
- **Comprehensive pytest suite**: Validates boundary conditions, missing element searches, out-of-bounds error handling, empty list behavior, and reversal functionality.
