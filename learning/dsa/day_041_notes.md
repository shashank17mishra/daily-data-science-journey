# Day 041: Doubly Linked List & LRU Cache

## Overview
This exercise focuses on implementing a Least Recently Used (LRU) Cache, a common data structure used in computer science to manage limited memory resources. The LRU Cache will be built upon a custom Doubly Linked List (DLL) and a hash map (Python dictionary). The DLL will maintain the order of items based on their recency of use, while the hash map will provide O(1) average time complexity for key lookups. You will implement the core components: a DoublyLinkedListNode, a DoublyLinkedList, and the LRUCache itself, ensuring efficient `get` and `put` operations.

## Objectives
- Understand algorithmic mechanics of Doubly Linked List & LRU Cache.
- Implement unit tests for edge cases.

## Key Concepts
The LRU Cache is a fundamental data structure for managing limited memory, ensuring that the most recently accessed items are kept readily available. This implementation combines two core data structures:

1.  **Doubly Linked List (DLL)**: A DLL is used to maintain the order of items based on their recency of use. The head of the list represents the Most Recently Used (MRU) item, and the tail represents the Least Recently Used (LRU) item. Key operations on the DLL include:
    *   `add_front(node)`: Adds a new node to the head, making it MRU.
    *   `remove_node(node)`: Removes a specific node from anywhere in the list. This is crucial for moving an existing node or evicting the tail.
    *   `move_to_front(node)`: A composite operation that first removes a node and then adds it back to the front. This is called when an item is accessed or updated.
    *   `remove_tail()`: Removes the node at the tail, which is the LRU item, for eviction.

2.  **Hash Map (Python Dictionary)**: A dictionary (`self.cache`) maps each key to its corresponding `DoublyLinkedListNode` object. This allows for O(1) average time complexity to quickly find a node given its key.

**How LRUCache Operations Work:**

*   **`get(key)`**: If the key exists in `self.cache`, we retrieve its node. Since this item has just been accessed, it becomes the MRU. We call `self.dll.move_to_front(node)` to update its position in the DLL. The value is then returned. If the key is not found, -1 is returned.
*   **`put(key, value)`**: 
    *   **If `key` already exists**: We retrieve the existing node from `self.cache`, update its `value`, and then call `self.dll.move_to_front(node)` to mark it as MRU.
    *   **If `key` does not exist**: 
        *   We first check if the cache has reached its `capacity`. If it has, we must evict the LRU item. This is done by calling `self.dll.remove_tail()`, which returns the tail node. We then remove this evicted item's key from `self.cache`.
        *   A new `DoublyLinkedListNode` is created with the given `key` and `value`.
        *   This new node is added to the front of the DLL using `self.dll.add_front(new_node)`.
        *   Finally, the new node is added to `self.cache` with its key.

This combination ensures that both `get` and `put` operations achieve an average time complexity of O(1), which is optimal for a cache system. The provided tests cover various scenarios, including basic operations, eviction, updating existing keys, and edge cases like a cache with capacity one or an empty list.
