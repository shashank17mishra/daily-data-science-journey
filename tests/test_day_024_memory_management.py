"""
Unit tests for Day 024: Memory Management & Garbage Collection.
"""

import gc
import pytest
from learning.python.day_024_memory_management import (
    get_ref_count,
    Node,
    cleanup_circular_references,
    WeakCache,
    ResourceTracker,
    get_deep_size,
)


class DummyObject:
    """Helper class for reference count and GC lifecycle tests."""
    pass


def test_get_ref_count():
    """Verifies reference count tracking and delta increments."""
    obj = DummyObject()
    base_count = get_ref_count(obj)
    assert base_count >= 1

    ref2 = obj
    assert get_ref_count(obj) == base_count + 1

    ref3 = obj
    assert get_ref_count(obj) == base_count + 2

    del ref2
    assert get_ref_count(obj) == base_count + 1

    del ref3
    assert get_ref_count(obj) == base_count


def test_circular_reference_cleanup():
    """Verifies that circular references are properly cleaned up by cyclic GC."""
    gc.collect()
    gc.disable()
    try:
        node_a = Node("A")
        node_b = Node("B")
        node_a.link(node_b)

        del node_a
        del node_b

        collected = cleanup_circular_references()
        assert collected >= 2
    finally:
        gc.enable()


def test_weak_cache_retrieval_and_gc():
    """Verifies weak cache behavior before and after garbage collection."""
    cache = WeakCache()
    item1 = DummyObject()
    item2 = DummyObject()

    cache.set("k1", item1)
    cache.set("k2", item2)

    assert cache.contains("k1")
    assert cache.contains("k2")
    assert len(cache) == 2
    assert cache.get("k1") is item1
    assert cache.get("k2") is item2

    # Dropping item1 should remove it from weak cache once collected
    del item1
    gc.collect()

    assert not cache.contains("k1")
    assert cache.get("k1") is None
    assert cache.contains("k2")
    assert len(cache) == 1

    del item2
    gc.collect()
    assert len(cache) == 0


def test_resource_tracker_explicit_close():
    """Verifies explicit resource closing and finalizer deactivation."""
    ResourceTracker.clear_registry()
    tracker = ResourceTracker("res-explicit-1")
    assert tracker.is_alive
    status = ResourceTracker.get_resource_status("res-explicit-1")
    assert status is not None
    assert status["status"] == "open"

    tracker.close()
    assert not tracker.is_alive
    status = ResourceTracker.get_resource_status("res-explicit-1")
    assert status is not None
    assert status["status"] == "closed"
    assert status["closed_via"] == "explicit"


def test_resource_tracker_finalizer_on_gc():
    """Verifies that finalizer executes automatically when object is collected by GC."""
    ResourceTracker.clear_registry()

    tracker = ResourceTracker("res-gc-1")
    fin = tracker._finalizer
    assert fin.alive

    del tracker
    gc.collect()

    assert not fin.alive
    status = ResourceTracker.get_resource_status("res-gc-1")
    assert status is not None
    assert status["status"] == "closed"
    assert status["closed_via"] == "gc"


def test_get_deep_size():
    """Verifies deep size calculation on nested structures and cyclic objects."""
    data = {
        "numbers": [1, 2, 3, 4],
        "nested": {"key": "value"},
    }
    size = get_deep_size(data)
    assert size > 0

    # Cyclic data structure should not recurse infinitely
    cycle_list = []
    cycle_list.append(cycle_list)
    cyclic_size = get_deep_size(cycle_list)
    assert cyclic_size > 0
