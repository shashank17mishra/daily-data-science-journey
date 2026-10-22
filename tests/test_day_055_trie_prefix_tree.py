"""Tests for advanced Trie implementation."""

import pytest
from learning.dsa.day_055_trie_prefix_tree import Trie


@pytest.fixture
def sample_trie():
    trie = Trie()
    words = ["apple", "app", "application", "apt", "banana", "band", "bandwidth", "bat"]
    for w in words:
        trie.insert(w)
    return trie


def test_insert_and_search(sample_trie):
    assert sample_trie.search("apple") is True
    assert sample_trie.search("app") is True
    assert sample_trie.search("application") is True
    assert sample_trie.search("appl") is False
    assert sample_trie.search("orange") is False


def test_starts_with(sample_trie):
    assert sample_trie.starts_with("app") is True
    assert sample_trie.starts_with("ban") is True
    assert sample_trie.starts_with("z") is False


def test_empty_string_handling():
    trie = Trie()
    trie.insert("")
    assert trie.search("") is False
    assert trie.starts_with("") is True
    assert trie.count_words_with_prefix("") == 0


def test_prefix_counts(sample_trie):
    assert sample_trie.count_words_with_prefix("app") == 3
    assert sample_trie.count_words_with_prefix("ban") == 3
    assert sample_trie.count_words_with_prefix("band") == 2
    assert sample_trie.count_words_with_prefix("nonexistent") == 0


def test_autocomplete(sample_trie):
    results = sample_trie.autocomplete("app")
    assert results == ["app", "apple", "application"]

    limited = sample_trie.autocomplete("app", limit=2)
    assert limited == ["app", "apple"]

    no_match = sample_trie.autocomplete("xyz")
    assert no_match == []


def test_wildcard_pattern_search(sample_trie):
    assert sample_trie.search_pattern("b.n.n.") == ["banana"]
    assert sample_trie.search_pattern("a..") == ["app", "apt"]
    assert sample_trie.search_pattern("ba..") == ["band"]


def test_deletion_and_node_cleanup(sample_trie):
    assert sample_trie.delete("app") is True
    assert sample_trie.search("app") is False
    assert sample_trie.search("apple") is True
    assert sample_trie.search("application") is True
    assert sample_trie.count_words_with_prefix("app") == 2

    assert sample_trie.delete("notpresent") is False
    assert sample_trie.delete("appl") is False

    assert sample_trie.delete("application") is True
    assert sample_trie.search("application") is False
    assert sample_trie.count_words_with_prefix("app") == 1


def test_complete_deletion():
    trie = Trie()
    trie.insert("cat")
    trie.insert("car")

    assert trie.delete("cat") is True
    assert "t" not in trie.root.children["c"].children
    assert trie.search("car") is True

    assert trie.delete("car") is True
    assert "c" not in trie.root.children
    assert trie.count_words_with_prefix("") == 0
