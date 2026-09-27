import pytest
from learning.dsa.day_031_big_o_complexity import (
    OperationCounter,
    TwoSumSolvers,
    analyze_complexity,
)


def test_operation_counter():
    counter = OperationCounter()
    counter.count_comparison(3)
    counter.count_allocation(2)
    counter.count_lookup(5)

    summary = counter.summary()
    assert summary["comparisons"] == 3
    assert summary["allocations"] == 2
    assert summary["lookups"] == 5
    assert summary["total_time_ops"] == 8
    assert summary["auxiliary_space_ops"] == 2

    counter.reset()
    assert counter.summary()["total_time_ops"] == 0


@pytest.mark.parametrize("solver_name", ["brute_force", "sorted_two_pointers", "hash_map"])
def test_solvers_basic_match(solver_name):
    solver = getattr(TwoSumSolvers, solver_name)
    nums = [2, 7, 11, 15]
    target = 9
    result = solver(nums, target)
    assert result is not None
    i, j = result
    assert nums[i] + nums[j] == target


@pytest.mark.parametrize("solver_name", ["brute_force", "sorted_two_pointers", "hash_map"])
def test_solvers_no_match(solver_name):
    solver = getattr(TwoSumSolvers, solver_name)
    nums = [1, 2, 3, 4]
    target = 100
    result = solver(nums, target)
    assert result is None


@pytest.mark.parametrize("solver_name", ["brute_force", "sorted_two_pointers", "hash_map"])
def test_solvers_edge_cases(solver_name):
    solver = getattr(TwoSumSolvers, solver_name)
    # Empty list
    assert solver([], 5) is None
    # Single element
    assert solver([5], 5) is None
    # Duplicates sum to target
    nums_dup = [3, 3]
    res_dup = solver(nums_dup, 6)
    assert res_dup is not None
    assert nums_dup[res_dup[0]] + nums_dup[res_dup[1]] == 6
    # Negative numbers
    nums_neg = [-5, -2, 3, 8]
    res_neg = solver(nums_neg, 1)
    assert res_neg is not None
    assert nums_neg[res_neg[0]] + nums_neg[res_neg[1]] == 1


def test_time_complexity_growth():
    nums = list(range(100))
    target = 197  # Last two elements 98 + 99
    analysis = analyze_complexity(nums, target)

    brute_ops = analysis["brute_force"]["metrics"]["total_time_ops"]
    hash_ops = analysis["hash_map"]["metrics"]["total_time_ops"]

    # Brute force on 100 elements searching till end should perform around 100*99/2 = 4950 ops
    # Hash map should perform around 100 lookups
    assert brute_ops > 4000
    assert hash_ops <= 100
    assert brute_ops > hash_ops * 40


def test_space_complexity_tradeoff():
    nums = list(range(50))
    target = 97
    analysis = analyze_complexity(nums, target)

    brute_space = analysis["brute_force"]["metrics"]["auxiliary_space_ops"]
    hash_space = analysis["hash_map"]["metrics"]["auxiliary_space_ops"]

    # Brute force allocates 0 auxiliary memory items
    # Hash map allocates items proportional to N
    assert brute_space == 0
    assert hash_space > 0
