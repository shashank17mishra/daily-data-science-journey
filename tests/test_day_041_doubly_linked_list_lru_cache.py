import pytest
from learning.dsa.day_041_doubly_linked_list_lru_cache import DoublyLinkedListNode, DoublyLinkedList, LRUCache

# --- DoublyLinkedListNode Tests ---
def test_dll_node_initialization():
    node = DoublyLinkedListNode(1, 10)
    assert node.key == 1
    assert node.value == 10
    assert node.prev is None
    assert node.next is None

# --- DoublyLinkedList Tests ---
def test_dll_initialization():
    dll = DoublyLinkedList()
    assert dll.head is None
    assert dll.tail is None
    assert dll.size == 0
    assert dll.get_nodes_in_order() == []

def test_dll_add_front_single_node():
    dll = DoublyLinkedList()
    node1 = DoublyLinkedListNode(1, 10)
    dll.add_front(node1)
    assert dll.head == node1
    assert dll.tail == node1
    assert dll.size == 1
    assert node1.prev is None
    assert node1.next is None
    assert dll.get_nodes_in_order() == [(1, 10)]

def test_dll_add_front_multiple_nodes():
    dll = DoublyLinkedList()
    node1 = DoublyLinkedListNode(1, 10)
    node2 = DoublyLinkedListNode(2, 20)
    node3 = DoublyLinkedListNode(3, 30)

    dll.add_front(node1) # (1,10)
    dll.add_front(node2) # (2,20) -> (1,10)
    dll.add_front(node3) # (3,30) -> (2,20) -> (1,10)

    assert dll.head == node3
    assert dll.tail == node1
    assert dll.size == 3
    assert dll.get_nodes_in_order() == [(3, 30), (2, 20), (1, 10)]

    assert node3.prev is None
    assert node3.next == node2
    assert node2.prev == node3
    assert node2.next == node1
    assert node1.prev == node2
    assert node1.next is None

def test_dll_remove_node_middle():
    dll = DoublyLinkedList()
    node1 = DoublyLinkedListNode(1, 10)
    node2 = DoublyLinkedListNode(2, 20)
    node3 = DoublyLinkedListNode(3, 30)
    dll.add_front(node1) # (1,10)
    dll.add_front(node2) # (2,20) -> (1,10)
    dll.add_front(node3) # (3,30) -> (2,20) -> (1,10)

    removed_node = dll.remove_node(node2) # (3,30) -> (1,10)
    assert removed_node == node2
    assert dll.size == 2
    assert dll.head == node3
    assert dll.tail == node1
    assert dll.get_nodes_in_order() == [(3, 30), (1, 10)]
    assert node3.next == node1
    assert node1.prev == node3
    assert node2.prev is None
    assert node2.next is None

def test_dll_remove_node_front():
    dll = DoublyLinkedList()
    node1 = DoublyLinkedListNode(1, 10)
    node2 = DoublyLinkedListNode(2, 20)
    dll.add_front(node1) # (1,10)
    dll.add_front(node2) # (2,20) -> (1,10)

    removed_node = dll.remove_node(node2) # (1,10)
    assert removed_node == node2
    assert dll.size == 1
    assert dll.head == node1
    assert dll.tail == node1
    assert dll.get_nodes_in_order() == [(1, 10)]
    assert node1.prev is None
    assert node1.next is None
    assert node2.prev is None
    assert node2.next is None

def test_dll_remove_node_end():
    dll = DoublyLinkedList()
    node1 = DoublyLinkedListNode(1, 10)
    node2 = DoublyLinkedListNode(2, 20)
    dll.add_front(node1) # (1,10)
    dll.add_front(node2) # (2,20) -> (1,10)

    removed_node = dll.remove_node(node1) # (2,20)
    assert removed_node == node1
    assert dll.size == 1
    assert dll.head == node2
    assert dll.tail == node2
    assert dll.get_nodes_in_order() == [(2, 20)]
    assert node2.prev is None
    assert node2.next is None
    assert node1.prev is None
    assert node1.next is None

def test_dll_remove_only_node():
    dll = DoublyLinkedList()
    node1 = DoublyLinkedListNode(1, 10)
    dll.add_front(node1) # (1,10)

    removed_node = dll.remove_node(node1) # ()
    assert removed_node == node1
    assert dll.size == 0
    assert dll.head is None
    assert dll.tail is None
    assert dll.get_nodes_in_order() == []
    assert node1.prev is None
    assert node1.next is None

def test_dll_move_to_front():
    dll = DoublyLinkedList()
    node1 = DoublyLinkedListNode(1, 10)
    node2 = DoublyLinkedListNode(2, 20)
    node3 = DoublyLinkedListNode(3, 30)
    dll.add_front(node1) # (1,10)
    dll.add_front(node2) # (2,20) -> (1,10)
    dll.add_front(node3) # (3,30) -> (2,20) -> (1,10)

    dll.move_to_front(node1) # (1,10) -> (3,30) -> (2,20)
    assert dll.get_nodes_in_order() == [(1, 10), (3, 30), (2, 20)]
    assert dll.head == node1
    assert dll.tail == node2
    assert dll.size == 3

    dll.move_to_front(node2) # (2,20) -> (1,10) -> (3,30)
    assert dll.get_nodes_in_order() == [(2, 20), (1, 10), (3, 30)]
    assert dll.head == node2
    assert dll.tail == node3
    assert dll.size == 3

    dll.move_to_front(node2) # Already at front, no change in order
    assert dll.get_nodes_in_order() == [(2, 20), (1, 10), (3, 30)]
    assert dll.head == node2
    assert dll.tail == node3
    assert dll.size == 3

def test_dll_remove_tail():
    dll = DoublyLinkedList()
    node1 = DoublyLinkedListNode(1, 10)
    node2 = DoublyLinkedListNode(2, 20)
    node3 = DoublyLinkedListNode(3, 30)
    dll.add_front(node1) # (1,10)
    dll.add_front(node2) # (2,20) -> (1,10)
    dll.add_front(node3) # (3,30) -> (2,20) -> (1,10)

    removed_tail = dll.remove_tail() # (3,30) -> (2,20)
    assert removed_tail == node1
    assert dll.size == 2
    assert dll.head == node3
    assert dll.tail == node2
    assert dll.get_nodes_in_order() == [(3, 30), (2, 20)]
    assert node1.prev is None
    assert node1.next is None

    removed_tail = dll.remove_tail() # (3,30)
    assert removed_tail == node2
    assert dll.size == 1
    assert dll.head == node3
    assert dll.tail == node3
    assert dll.get_nodes_in_order() == [(3, 30)]

def test_dll_remove_tail_single_node():
    dll = DoublyLinkedList()
    node1 = DoublyLinkedListNode(1, 10)
    dll.add_front(node1) # (1,10)

    removed_tail = dll.remove_tail() # ()
    assert removed_tail == node1
    assert dll.size == 0
    assert dll.head is None
    assert dll.tail is None
    assert dll.get_nodes_in_order() == []

def test_dll_remove_tail_empty_list():
    dll = DoublyLinkedList()
    removed_tail = dll.remove_tail()
    assert removed_tail is None
    assert dll.size == 0
    assert dll.head is None
    assert dll.tail is None
    assert dll.get_nodes_in_order() == []

# --- LRUCache Tests ---
def test_lru_cache_initialization():
    cache = LRUCache(5)
    assert cache.capacity == 5
    assert len(cache.cache) == 0
    assert cache.dll.size == 0

def test_lru_cache_invalid_capacity():
    with pytest.raises(ValueError, match="Capacity must be a positive integer."):
        LRUCache(0)
    with pytest.raises(ValueError, match="Capacity must be a positive integer."):
        LRUCache(-1)
    with pytest.raises(ValueError, match="Capacity must be a positive integer."):
        LRUCache("abc")

def test_lru_cache_put_and_get_basic():
    cache = LRUCache(2)
    cache.put(1, 10) # DLL: (1,10)
    cache.put(2, 20) # DLL: (2,20) -> (1,10)

    assert cache.get(1) == 10 # Access 1, moves to front. DLL: (1,10) -> (2,20)
    assert cache.get(2) == 20 # Access 2, moves to front. DLL: (2,20) -> (1,10)
    assert cache.dll.get_nodes_in_order() == [(2, 20), (1, 10)]
    assert len(cache.cache) == 2
    assert cache.dll.size == 2

def test_lru_cache_eviction():
    cache = LRUCache(2)
    cache.put(1, 10) # DLL: (1,10)
    cache.put(2, 20) # DLL: (2,20) -> (1,10)
    cache.put(3, 30) # Evicts (1,10). DLL: (3,30) -> (2,20)

    assert cache.get(1) == -1 # 1 should be evicted
    assert cache.get(2) == 20 # 2 should still be there, moves to front. DLL: (2,20) -> (3,30)
    assert cache.get(3) == 30 # 3 should still be there, moves to front. DLL: (3,30) -> (2,20)
    assert cache.dll.get_nodes_in_order() == [(3, 30), (2, 20)]
    assert len(cache.cache) == 2
    assert cache.dll.size == 2

def test_lru_cache_update_existing_key():
    cache = LRUCache(2)
    cache.put(1, 10) # DLL: (1,10)
    cache.put(2, 20) # DLL: (2,20) -> (1,10)
    assert cache.get(1) == 10 # Access 1, moves to front. DLL: (1,10) -> (2,20)
    cache.put(3, 30) # Evicts (2,20). DLL: (3,30) -> (1,10)
    assert cache.get(1) == 10 # Access 1, moves to front. DLL: (1,10) -> (3,30)
    assert cache.get(3) == 30 # Access 3, moves to front. DLL: (3,30) -> (1,10)
    assert cache.get(2) == -1 # 2 was evicted

    # Now, update an existing key (1)
    cache.put(1, 100) # Update (1,10) to (1,100), moves to front. DLL: (1,100) -> (3,30)
    assert cache.get(1) == 100
    assert cache.dll.get_nodes_in_order() == [(1, 100), (3, 30)]
    assert len(cache.cache) == 2
    assert cache.dll.size == 2

    # Update another existing key (3)
    cache.put(3, 300) # Update (3,30) to (3,300), moves to front. DLL: (3,300) -> (1,100)
    assert cache.get(3) == 300
    assert cache.dll.get_nodes_in_order() == [(3, 300), (1, 100)]
    assert len(cache.cache) == 2
    assert cache.dll.size == 2

def test_lru_cache_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 10) # DLL: (1,10)
    assert cache.get(1) == 10
    assert cache.dll.get_nodes_in_order() == [(1, 10)]

    cache.put(2, 20) # Evicts (1,10). DLL: (2,20)
    assert cache.get(1) == -1
    assert cache.get(2) == 20
    assert cache.dll.get_nodes_in_order() == [(2, 20)]
    assert len(cache.cache) == 1
    assert cache.dll.size == 1

    cache.put(2, 200) # Update (2,20) to (2,200). DLL: (2,200)
    assert cache.get(2) == 200
    assert cache.dll.get_nodes_in_order() == [(2, 200)]
    assert len(cache.cache) == 1
    assert cache.dll.size == 1

def test_lru_cache_access_order_on_get():
    cache = LRUCache(3)
    cache.put(1, 10) # (1,10)
    cache.put(2, 20) # (2,20) -> (1,10)
    cache.put(3, 30) # (3,30) -> (2,20) -> (1,10)
    assert cache.dll.get_nodes_in_order() == [(3, 30), (2, 20), (1, 10)]

    cache.get(1) # Access 1. (1,10) -> (3,30) -> (2,20)
    assert cache.dll.get_nodes_in_order() == [(1, 10), (3, 30), (2, 20)]

    cache.get(2) # Access 2. (2,20) -> (1,10) -> (3,30)
    assert cache.dll.get_nodes_in_order() == [(2, 20), (1, 10), (3, 30)]

    cache.get(3) # Access 3. (3,30) -> (2,20) -> (1,10)
    assert cache.dll.get_nodes_in_order() == [(3, 30), (2, 20), (1, 10)]

def test_lru_cache_size_consistency():
    cache = LRUCache(3)
    assert len(cache.cache) == 0
    assert cache.dll.size == 0

    cache.put(1, 10)
    assert len(cache.cache) == 1
    assert cache.dll.size == 1

    cache.put(2, 20)
    assert len(cache.cache) == 2
    assert cache.dll.size == 2

    cache.put(3, 30)
    assert len(cache.cache) == 3
    assert cache.dll.size == 3

    cache.put(4, 40) # Evicts 1
    assert len(cache.cache) == 3
    assert cache.dll.size == 3
    assert cache.get(1) == -1

    cache.get(2) # Access 2
    assert len(cache.cache) == 3
    assert cache.dll.size == 3

def test_lru_cache_non_existent_key():
    cache = LRUCache(2)
    cache.put(1, 10)
    assert cache.get(99) == -1
    assert cache.get(1) == 10 # Ensure existing key still works

def test_lru_cache_put_multiple_evictions():
    cache = LRUCache(2)
    cache.put(1, 10) # (1,10)
    cache.put(2, 20) # (2,20) -> (1,10)
    assert cache.dll.get_nodes_in_order() == [(2, 20), (1, 10)]

    cache.put(3, 30) # Evicts (1,10). (3,30) -> (2,20)
    assert cache.get(1) == -1
    assert cache.dll.get_nodes_in_order() == [(3, 30), (2, 20)]

    cache.put(4, 40) # Evicts (2,20). (4,40) -> (3,30)
    assert cache.get(2) == -1
    assert cache.dll.get_nodes_in_order() == [(4, 40), (3, 30)]

    assert cache.get(3) == 30 # Access 3. (3,30) -> (4,40)
    assert cache.dll.get_nodes_in_order() == [(3, 30), (4, 40)]

    cache.put(5, 50) # Evicts (4,40). (5,50) -> (3,30)
    assert cache.get(4) == -1
    assert cache.dll.get_nodes_in_order() == [(5, 50), (3, 30)]

def test_lru_cache_get_non_existent_after_eviction():
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    cache.put(3, 30) # Evicts 1
    assert cache.get(1) == -1
    assert cache.get(2) == 20
    assert cache.get(3) == 30
    assert cache.dll.get_nodes_in_order() == [(3, 30), (2, 20)] # 3 accessed, then 2 accessed.
