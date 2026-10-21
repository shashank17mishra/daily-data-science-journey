import pytest
from learning.dsa.day_054_bit_manipulation_operations import (
    count_set_bits,
    is_power_of_two,
    find_single_number_twice,
    find_single_number_thrice
)

# --- Tests for count_set_bits ---
def test_count_set_bits_basic():
    assert count_set_bits(0) == 0
    assert count_set_bits(1) == 1  # 0b1
    assert count_set_bits(2) == 1  # 0b10
    assert count_set_bits(3) == 2  # 0b11
    assert count_set_bits(7) == 3  # 0b111
    assert count_set_bits(8) == 1  # 0b1000

def test_count_set_bits_large_numbers():
    assert count_set_bits(255) == 8  # 0b11111111
    assert count_set_bits(1024) == 1 # 0b10000000000
    assert count_set_bits((1 << 30) - 1) == 30 # All bits up to 2^30-1 are set

def test_count_set_bits_edge_cases():
    with pytest.raises(ValueError):
        count_set_bits(-1)
    with pytest.raises(ValueError):
        count_set_bits(-100)

# --- Tests for is_power_of_two ---
def test_is_power_of_two_true():
    assert is_power_of_two(1) is True
    assert is_power_of_two(2) is True
    assert is_power_of_two(4) is True
    assert is_power_of_two(16) is True
    assert is_power_of_two(1024) is True
    assert is_power_of_two(2**30) is True

def test_is_power_of_two_false():
    assert is_power_of_two(0) is False
    assert is_power_of_two(3) is False
    assert is_power_of_two(6) is False
    assert is_power_of_two(15) is False
    assert is_power_of_two(1023) is False
    assert is_power_of_two(-2) is False # Negative numbers are not powers of two

# --- Tests for find_single_number_twice ---
def test_find_single_number_twice_basic():
    assert find_single_number_twice([2, 2, 1]) == 1
    assert find_single_number_twice([4, 1, 2, 1, 2]) == 4
    assert find_single_number_twice([1]) == 1

def test_find_single_number_twice_large_numbers():
    assert find_single_number_twice([100000, 200000, 100000, 300000, 200000]) == 300000
    assert find_single_number_twice([2**30, 2**30, 2**29]) == 2**29

def test_find_single_number_twice_negative_numbers():
    assert find_single_number_twice([-1, -1, -2]) == -2
    assert find_single_number_twice([-5, -5, 0]) == 0
    assert find_single_number_twice([-10, 20, -10, 20, -30]) == -30

def test_find_single_number_twice_edge_cases():
    assert find_single_number_twice([0, 0, 5]) == 5
    assert find_single_number_twice([5, 0, 5]) == 0
    assert find_single_number_twice([1, 1, 2, 2, 3, 3, 4]) == 4
    assert find_single_number_twice([1, 2, 3, 1, 2]) == 3

# --- Tests for find_single_number_thrice ---
def test_find_single_number_thrice_basic():
    assert find_single_number_thrice([2, 2, 3, 2]) == 3
    assert find_single_number_thrice([0, 1, 0, 0]) == 1
    assert find_single_number_thrice([1]) == 1

def test_find_single_number_thrice_large_numbers():
    assert find_single_number_thrice([10**9, 10**9, 10**9, 5 * 10**8]) == 5 * 10**8
    assert find_single_number_thrice([2**30, 2**30, 2**30, 2**29]) == 2**29

def test_find_single_number_thrice_negative_numbers():
    assert find_single_number_thrice([-1, -1, -1, -2]) == -2
    assert find_single_number_thrice([-5, -5, -5, 0]) == 0
    assert find_single_number_thrice([-10, -10, -10, 20, 20, 20, -30]) == -30
    assert find_single_number_thrice([-1, -1, -1, 2**31 - 1]) == 2**31 - 1 # Max positive 32-bit signed
    assert find_single_number_thrice([-1, -1, -1, -2**31]) == -2**31 # Min negative 32-bit signed

def test_find_single_number_thrice_edge_cases():
    assert find_single_number_thrice([0, 0, 0, 5]) == 5
    assert find_single_number_thrice([5, 5, 5, 0]) == 0
    assert find_single_number_thrice([1, 1, 1, 2, 2, 2, 3, 3, 3, 4]) == 4
    assert find_single_number_thrice([1, 2, 3, 1, 2, 3, 1, 2, 3, 4]) == 4
