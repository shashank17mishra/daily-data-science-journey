"""
Unit tests for 1D Dynamic Programming algorithms.
"""

import pytest
from learning.dsa.day_051_1d_dp import Advanced1DDP


class TestNumDecodings:
    def test_single_characters(self):
        assert Advanced1DDP.num_decodings("*") == 9
        assert Advanced1DDP.num_decodings("1") == 1
        assert Advanced1DDP.num_decodings("0") == 0
        assert Advanced1DDP.num_decodings("") == 0

    def test_wildcard_pairs(self):
        assert Advanced1DDP.num_decodings("1*") == 18
        assert Advanced1DDP.num_decodings("*1") == 11
        assert Advanced1DDP.num_decodings("**") == 96  # 9*9 + 15

    def test_invalid_leading_zeros(self):
        assert Advanced1DDP.num_decodings("06") == 0
        assert Advanced1DDP.num_decodings("0*") == 0

    def test_complex_string(self):
        assert Advanced1DDP.num_decodings("2*") == 15  # '2' + '*' (9) + '2*' (6: 21-26)


class TestMaxSumAfterPartitioning:
    def test_standard_case(self):
        arr = [1, 15, 7, 9, 2, 5, 10]
        assert Advanced1DDP.max_sum_after_partitioning(arr, 3) == 84

    def test_k_equals_one(self):
        arr = [1, 2, 3, 4]
        assert Advanced1DDP.max_sum_after_partitioning(arr, 1) == sum(arr)

    def test_k_larger_than_array(self):
        arr = [1, 10, 3]
        assert Advanced1DDP.max_sum_after_partitioning(arr, 5) == 30

    def test_empty_array(self):
        assert Advanced1DDP.max_sum_after_partitioning([], 3) == 0
        assert Advanced1DDP.max_sum_after_partitioning([1, 2], 0) == 0


class TestMinCostTickets:
    def test_standard_schedule(self):
        days = [1, 4, 6, 7, 8, 20]
        costs = [2, 7, 15]
        assert Advanced1DDP.min_cost_tickets(days, costs) == 11

    def test_month_pass_cheapest(self):
        days = list(range(1, 31))
        costs = [2, 7, 15]
        assert Advanced1DDP.min_cost_tickets(days, costs) == 15

    def test_single_day(self):
        days = [10]
        costs = [2, 7, 15]
        assert Advanced1DDP.min_cost_tickets(days, costs) == 2

    def test_empty_or_invalid_inputs(self):
        assert Advanced1DDP.min_cost_tickets([], [2, 7, 15]) == 0
        assert Advanced1DDP.min_cost_tickets([1, 2], [2, 7]) == 0
