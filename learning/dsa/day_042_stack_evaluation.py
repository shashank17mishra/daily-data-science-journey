"""
Day 042: Stack Data Structure & Expression Evaluation

This module provides a custom Stack data structure implementation along with
algorithms to convert and evaluate arithmetic expressions:
- Infix to Postfix conversion using Dijkstra's Shunting-Yard Algorithm.
- Postfix (Reverse Polish Notation) evaluation.
- Direct Infix expression evaluation.
"""

import math
from typing import Generic, List, TypeVar

T = TypeVar("T")


class StackError(Exception):
    """Custom exception raised for stack operations errors."""

    pass


class Stack(Generic[T]):
    """A generic LIFO (Last-In-First-Out) stack implementation."""

    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        """Push an item onto the top of the stack."""
        self._items.append(item)

    def pop(self) -> T:
        """Pop and return the top item from the stack.

        Raises:
            StackError: If the stack is empty.
        """
        if self.is_empty():
            raise StackError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self) -> T:
        """Return the top item without removing it.

        Raises:
            StackError: If the stack is empty.
        """
        if self.is_empty():
            raise StackError("Cannot peek at an empty stack.")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the stack is empty, False otherwise."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of items in the stack."""
        return len(self._items)

    def __len__(self) -> int:
        return self.size()

    def __repr__(self) -> str:
        return f"Stack({self._items})"


class ExpressionEvaluator:
    """Evaluates mathematical expressions using Stack data structures."""

    OPERATORS = {
        "+": (1, "L"),
        "-": (1, "L"),
        "*": (2, "L"),
        "/": (2, "L"),
        "^": (3, "R"),
    }

    @staticmethod
    def _apply_op(op: str, b: float, a: float) -> float:
        """Apply an operator on operands a and b (a op b)."""
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            if b == 0:
                raise ValueError("Division by zero error.")
            return a / b
        if op == "^":
            return math.pow(a, b)
        raise ValueError(f"Unsupported operator: {op}")

    @classmethod
    def tokenize(cls, expression: str) -> List[str]:
        """Tokenize an input mathematical expression string."""
        tokens: List[str] = []
        i = 0
        n = len(expression)

        while i < n:
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or char == ".":
                num_str = []
                dot_count = 0
                while i < n and (expression[i].isdigit() or expression[i] == "."):
                    if expression[i] == ".":
                        dot_count += 1
                        if dot_count > 1:
                            raise ValueError(
                                f"Invalid number format with multiple decimal points at index {i}"
                            )
                    num_str.append(expression[i])
                    i += 1
                tokens.append("".join(num_str))
                continue

            if char in cls.OPERATORS or char in "()":
                tokens.append(char)
                i += 1
                continue

            raise ValueError(f"Invalid character in expression: '{char}' at index {i}")

        return tokens

    @classmethod
    def infix_to_postfix(cls, expression: str) -> List[str]:
        """Convert an infix expression string or token list to postfix (RPN) tokens."""
        tokens = cls.tokenize(expression)
        output: List[str] = []
        operator_stack = Stack[str]()

        for token in tokens:
            if cls._is_number(token):
                output.append(token)
            elif token in cls.OPERATORS:
                prec_curr, assoc_curr = cls.OPERATORS[token]
                while not operator_stack.is_empty() and operator_stack.peek() in cls.OPERATORS:
                    top_op = operator_stack.peek()
                    prec_top, _ = cls.OPERATORS[top_op]

                    if (assoc_curr == "L" and prec_curr <= prec_top) or (
                        assoc_curr == "R" and prec_curr < prec_top
                    ):
                        output.append(operator_stack.pop())
                    else:
                        break
                operator_stack.push(token)
            elif token == "(":
                operator_stack.push(token)
            elif token == ")":
                while not operator_stack.is_empty() and operator_stack.peek() != "(":
                    output.append(operator_stack.pop())
                if operator_stack.is_empty():
                    raise ValueError("Mismatched parentheses: excess closing parenthesis.")
                operator_stack.pop()

        while not operator_stack.is_empty():
            top_token = operator_stack.pop()
            if top_token in "()":
                raise ValueError("Mismatched parentheses: unclosed opening parenthesis.")
            output.append(top_token)

        return output

    @classmethod
    def evaluate_postfix(cls, postfix_tokens: List[str]) -> float:
        """Evaluate a list of postfix (RPN) tokens."""
        val_stack = Stack[float]()

        for token in postfix_tokens:
            if cls._is_number(token):
                val_stack.push(float(token))
            elif token in cls.OPERATORS:
                if val_stack.size() < 2:
                    raise ValueError(
                        f"Invalid expression: insufficient operands for operator '{token}'."
                    )
                b = val_stack.pop()
                a = val_stack.pop()
                res = cls._apply_op(token, b, a)
                val_stack.push(res)
            else:
                raise ValueError(f"Invalid token in postfix expression: '{token}'")

        if val_stack.size() != 1:
            raise ValueError("Invalid expression: excess operands.")

        return val_stack.pop()

    @classmethod
    def evaluate_infix(cls, expression: str) -> float:
        """Evaluate an infix expression directly by converting to postfix first."""
        postfix_tokens = cls.infix_to_postfix(expression)
        return cls.evaluate_postfix(postfix_tokens)

    @staticmethod
    def _is_number(token: str) -> bool:
        try:
            float(token)
            return True
        except ValueError:
            return False
