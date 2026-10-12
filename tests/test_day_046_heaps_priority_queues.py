import random
import pytest
from learning.dsa.day_046_heaps_priority_queues import IndexedMinHeap


def test_empty_heap_operations():
    heap = IndexedMinHeap()
    assert len(heap) == 0
    assert heap.is_empty()
    assert not heap.contains("node_a")

    with pytest.raises(IndexError, match="Peek from an empty heap"):
        heap.peek()

    with pytest.raises(IndexError, match="Pop from an empty heap"):
        heap.pop()


def test_push_and_pop_ordering():
    heap = IndexedMinHeap()
    items = [("C", 3.0), ("A", 1.0), ("B", 2.0), ("E", 5.0), ("D", 4.0)]
    for key, prio in items:
        heap.push(key, prio)

    assert len(heap) == 5
    assert heap.peek() == ("A", 1.0)

    popped = []
    while not heap.is_empty():
        popped.append(heap.pop())

    expected = [("A", 1.0), ("B", 2.0), ("C", 3.0), ("D", 4.0), ("E", 5.0)]
    assert popped == expected


def test_duplicate_push_raises_error():
    heap = IndexedMinHeap()
    heap.push("task1", 10.0)
    with pytest.raises(ValueError, match="already exists"):
        heap.push("task1", 5.0)


def test_get_priority_and_contains():
    heap = IndexedMinHeap()
    heap.push("node1", 15.5)
    heap.push("node2", 7.2)

    assert heap.contains("node1")
    assert heap.contains("node2")
    assert not heap.contains("node3")

    assert heap.get_priority("node1") == 15.5
    assert heap.get_priority("node2") == 7.2

    with pytest.raises(KeyError, match="not found"):
        heap.get_priority("node3")


def test_update_priority():
    heap = IndexedMinHeap()
    heap.push("A", 10.0)
    heap.push("B", 20.0)
    heap.push("C", 30.0)

    # Decrease priority of C to 5.0 (C becomes root)
    heap.update_priority("C", 5.0)
    assert heap.peek() == ("C", 5.0)
    assert heap.get_priority("C") == 5.0

    # Increase priority of C to 50.0 (A becomes root again)
    heap.update_priority("C", 50.0)
    assert heap.peek() == ("A", 10.0)

    with pytest.raises(KeyError, match="not found"):
        heap.update_priority("missing_key", 100.0)


def test_delete_arbitrary_key():
    heap = IndexedMinHeap()
    heap.push("A", 10)
    heap.push("B", 20)
    heap.push("C", 30)
    heap.push("D", 40)

    # Delete inner node
    deleted = heap.delete("B")
    assert deleted == ("B", 20)
    assert not heap.contains("B")
    assert len(heap) == 3

    # Delete root node
    deleted_root = heap.delete("A")
    assert deleted_root == ("A", 10)
    assert heap.peek() == ("C", 30)

    # Delete remaining nodes
    heap.delete("D")
    heap.delete("C")
    assert heap.is_empty()

    with pytest.raises(KeyError, match="not found"):
        heap.delete("nonexistent")


def test_randomized_stress_operations():
    heap = IndexedMinHeap()
    dict_ref = {}
    random.seed(42)

    # Populate 100 random keys
    for i in range(100):
        key = f"key_{i}"
        prio = random.uniform(0.0, 1000.0)
        heap.push(key, prio)
        dict_ref[key] = prio

    # Random updates and deletions
    for i in range(50):
        key = f"key_{random.randint(0, 99)}"
        if heap.contains(key):
            if i % 2 == 0:
                new_prio = random.uniform(0.0, 1000.0)
                heap.update_priority(key, new_prio)
                dict_ref[key] = new_prio
            else:
                heap.delete(key)
                del dict_ref[key]

    # Verify popped items strictly match sorted dictionary contents
    popped_items = []
    while not heap.is_empty():
        popped_items.append(heap.pop())

    expected_items = sorted(dict_ref.items(), key=lambda x: x[1])
    assert popped_items == expected_items
