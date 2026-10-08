import pytest
from learning.dsa.day_042_stack_evaluation import ExpressionEvaluator, Stack, StackError


def test_stack_basic_operations():
    s = Stack[int]()
    assert s.is_empty()
    assert len(s) == 0

    s.push(10)
    s.push(20)
    assert not s.is_empty()
    assert len(s) == 2
    assert s.peek() == 20
    assert s.pop() == 20
    assert s.pop() == 10
    assert s.is_empty()


def test_stack_empty_pop_peek_raises():
    s = Stack[str]()
    with pytest.raises(StackError, match="Cannot pop from an empty stack."):
        s.pop()

    with pytest.raises(StackError, match="Cannot peek at an empty stack."):
        s.peek()


def test_tokenize_valid():
    tokens = ExpressionEvaluator.tokenize("3 + 45.5 * (10 - 2)")
    assert tokens == ["3", "+", "45.5", "*", "(", "10", "-", "2", ")"]


def test_tokenize_invalid_character():
    with pytest.raises(ValueError, match="Invalid character"):
        ExpressionEvaluator.tokenize("3 + x * 2")


def test_tokenize_invalid_number_format():
    with pytest.raises(ValueError, match="Invalid number format"):
        ExpressionEvaluator.tokenize("3.14.15 + 2")


def test_infix_to_postfix_basic():
    postfix = ExpressionEvaluator.infix_to_postfix("3 + 4 * 2 / (1 - 5) ^ 2")
    expected = ["3", "4", "2", "*", "1", "5", "-", "2", "^", "/", "+"]
    assert postfix == expected


def test_infix_to_postfix_associativity():
    postfix = ExpressionEvaluator.infix_to_postfix("2 ^ 3 ^ 2")
    assert postfix == ["2", "3", "2", "^", "^"]


def test_infix_mismatched_parentheses():
    with pytest.raises(ValueError, match="excess closing parenthesis"):
        ExpressionEvaluator.infix_to_postfix("(3 + 4))")

    with pytest.raises(ValueError, match="unclosed opening parenthesis"):
        ExpressionEvaluator.infix_to_postfix("((3 + 4)")


def test_evaluate_postfix_basic():
    res = ExpressionEvaluator.evaluate_postfix(["3", "4", "2", "*", "+"])
    assert res == 11.0


def test_evaluate_infix_expressions():
    assert ExpressionEvaluator.evaluate_infix("3 + 4 * 2") == 11.0
    assert ExpressionEvaluator.evaluate_infix("(3 + 4) * 2") == 14.0
    assert ExpressionEvaluator.evaluate_infix("2 ^ 3 ^ 2") == 512.0
    assert ExpressionEvaluator.evaluate_infix("100 / 4 / 5") == 5.0


def test_evaluate_infix_division_by_zero():
    with pytest.raises(ValueError, match="Division by zero error."):
        ExpressionEvaluator.evaluate_infix("10 / (5 - 5)")


def test_evaluate_postfix_invalid_operands():
    with pytest.raises(ValueError, match="insufficient operands"):
        ExpressionEvaluator.evaluate_postfix(["3", "+"])

    with pytest.raises(ValueError, match="excess operands"):
        ExpressionEvaluator.evaluate_postfix(["3", "4", "5", "+"])
