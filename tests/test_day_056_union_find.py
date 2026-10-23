"""
Unit tests for the Disjoint-Set (Union-Find) implementation.
"""

import pytest
from learning.dsa.day_056_union_find import UnionFind


def test_initialization():
    uf = UnionFind([1, 2, 3])
    assert len(uf) == 3
    assert uf.num_components == 3
    assert 1 in uf
    assert 4 not in uf


def test_add_duplicate_and_new():
    uf = UnionFind()
    assert uf.add("A") is True
    assert uf.add("A") is False
    assert len(uf) == 1
    assert uf.num_components == 1


def test_find_nonexistent():
    uf = UnionFind([1, 2])
    with pytest.raises(KeyError):
        uf.find(99)


def test_union_and_connected():
    uf = UnionFind(["a", "b", "c", "d"])
    assert uf.union("a", "b") is True
    assert uf.connected("a", "b") is True
    assert uf.num_components == 3

    assert uf.union("a", "b") is False
    assert uf.num_components == 3

    assert uf.connected("a", "c") is False
    assert uf.union("b", "c") is True
    assert uf.connected("a", "c") is True
    assert uf.num_components == 2


def test_auto_add_on_union():
    uf = UnionFind()
    assert uf.union("X", "Y") is True
    assert "X" in uf
    assert "Y" in uf
    assert uf.num_components == 1
    assert uf.get_component_size("X") == 2


def test_component_sizes():
    uf = UnionFind(list(range(10)))
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(3, 4)

    assert uf.get_component_size(0) == 3
    assert uf.get_component_size(2) == 3
    assert uf.get_component_size(4) == 2
    assert uf.get_component_size(5) == 1


def test_get_components():
    uf = UnionFind([1, 2, 3, 4])
    uf.union(1, 2)
    uf.union(3, 4)

    components = uf.get_components()
    assert len(components) == 2
    group_sizes = sorted([len(s) for s in components.values()])
    assert group_sizes == [2, 2]


def test_path_compression_mechanics():
    uf = UnionFind()
    for i in range(99):
        uf.union(i, i + 1)

    root = uf.find(0)
    assert uf.find(50) == root
    assert uf.get_component_size(0) == 100
    assert uf.num_components == 1


def test_heterogeneous_hashable_types():
    uf = UnionFind()
    uf.union(1, "one")
    uf.union((1, 2), "one")

    assert uf.connected(1, (1, 2)) is True
    assert uf.get_component_size("one") == 3
