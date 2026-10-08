# Day 042: Stack Data Structure & Expression Evaluation

## Overview
Implementation of a generic LIFO Stack data structure and an Expression Evaluator that handles tokenization, Infix-to-Postfix (Reverse Polish Notation) conversion via Dijkstra's Shunting-Yard Algorithm, and Postfix expression evaluation.

## Objectives
- Understand algorithmic mechanics of Stack Data Structure & Evaluation.
- Implement unit tests for edge cases.

## Key Concepts
A Stack is a Last-In, First-Out (LIFO) abstract data structure essential for managing state in expression parsing and function calls.

### Key Concepts:
1. **Generic Stack Data Structure**: Implemented using Python's list, supporting `push`, `pop`, `peek`, and size checks, wrapped in explicit exception safety (`StackError`).
2. **Shunting-Yard Algorithm**: Converts standard mathematical infix expressions (e.g., `3 + 4 * 2`) to postfix notation (Reverse Polish Notation: `3 4 2 * +`). It respects operator precedence (e.g., `*` before `+`) and associativity rules (left-associative for `+,-,*,/`, right-associative for `^`).
3. **Postfix Evaluation**: Evaluates Postfix expressions in $O(N)$ time complexity using an evaluation stack. Operands are pushed onto the stack, and when an operator is encountered, the top two operands are popped, evaluated, and the result is pushed back onto the stack.
4. **Robust Parsing & Error Handling**: Handles multi-digit integers, floating-point values, whitespace, mismatched parentheses, illegal syntax, and division-by-zero checks.
