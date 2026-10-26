"""Unit tests for the KMP Substring Search implementation."""

import pytest
from learning.python.day_059_kmp_substring_search import (
    compute_lps_array,
    kmp_contains,
    kmp_search,
)


def test_compute_lps_array_basic():
    assert compute_lps_array("") == []
    assert compute_lps_array("A") == [0]
    assert compute_lps_array("AAAA") == [0, 1, 2, 3]
    assert compute_lps_array("ABCDE") == [0, 0, 0, 0, 0]
    assert compute_lps_array("AABAACAABAA") == [0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5]


def test_kmp_search_single_match():
    text = "hello world"
    pattern = "world"
    assert kmp_search(text, pattern) == [6]


def test_kmp_search_multiple_matches():
    text = "ab ab ab ab"
    pattern = "ab"
    assert kmp_search(text, pattern) == [0, 3, 6, 9]


def test_kmp_search_overlapping_matches():
    text = "aaaaa"
    pattern = "aaa"
    assert kmp_search(text, pattern) == [0, 1, 2]


def test_kmp_search_no_match():
    text = "abcdefg"
    pattern = "xyz"
    assert kmp_search(text, pattern) == []


def test_kmp_search_edge_cases():
    assert kmp_search("", "abc") == []
    assert kmp_search("abc", "") == []
    assert kmp_search("", "") == []
    assert kmp_search("short", "longer_pattern") == []
    assert kmp_search("exact", "exact") == [0]


def test_kmp_contains():
    assert kmp_contains("banana", "ana") is True
    assert kmp_contains("banana", "apple") is False
    assert kmp_contains("banana", "") is False


def test_kmp_unicode_and_symbols():
    text = "hello 🌍 world 🌍"
    pattern = "🌍"
    assert kmp_search(text, pattern) == [6, 14]
    assert kmp_contains(text, pattern) is True
