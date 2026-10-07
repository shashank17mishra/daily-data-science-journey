class DoublyLinkedListNode:
    """
    Represents a node in a Doubly Linked List.
    Each node stores a key-value pair and references to the previous and next nodes.
    """
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """
    A custom Doubly Linked List implementation to manage the order of items
    in the LRU Cache. It supports adding to the front, removing a specific node,
    moving a node to the front, and removing the tail node.
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_front(self, node: DoublyLinkedListNode) -> None:
        """
        Adds a node to the front (head) of the list.
        This node becomes the most recently used.
        """
        if not node:
            return

        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    def remove_node(self, node: DoublyLinkedListNode) -> DoublyLinkedListNode:
        """
        Removes a specific node from the list.
        Handles cases for head, tail, and middle nodes.
        Returns the removed node.
        """
        if not node or self.size == 0:
            return None

        if node == self.head and node == self.tail: # Only one node
            self.head = None
            self.tail = None
        elif node == self.head: # Node is the head
            self.head = node.next
            if self.head: # Ensure head is not None if list becomes empty
                self.head.prev = None
        elif node == self.tail: # Node is the tail
            self.tail = node.prev
            if self.tail: # Ensure tail is not None if list becomes empty
                self.tail.next = None
        else: # Node is in the middle
            node.prev.next = node.next
            node.next.prev = node.prev
        
        node.prev = None # Clean up removed node's pointers
        node.next = None
        self.size -= 1
        return node

    def move_to_front(self, node: DoublyLinkedListNode) -> None:
        """
        Moves an existing node to the front (head) of the list.
        This is used when an item is accessed or updated, making it most recently used.
        """
        if not node or self.head == node: # Already at front or invalid node
            return
        
        self.remove_node(node)
        self.add_front(node)

    def remove_tail(self) -> DoublyLinkedListNode:
        """
        Removes and returns the tail node (least recently used).
        """
        if not self.tail:
            return None
        
        node_to_remove = self.tail
        return self.remove_node(node_to_remove)

    def get_nodes_in_order(self) -> list[tuple[int, int]]:
        """
        Helper method for testing: returns a list of (key, value) tuples
        from head to tail.
        """
        nodes = []
        current = self.head
        while current:
            nodes.append((current.key, current.value))
            current = current.next
        return nodes

class LRUCache:
    """
    Implements a Least Recently Used (LRU) Cache using a hash map (dictionary)
    and a Doubly Linked List.
    The hash map provides O(1) average time complexity for `get` and `put` operations.
    The Doubly Linked List maintains the order of usage, allowing O(1) removal
    of the least recently used item and O(1) movement of an item to the most
    recently used position.
    """
    def __init__(self, capacity: int):
        """
        Initializes the LRU Cache with a given capacity.
        :param capacity: The maximum number of key-value pairs the cache can hold.
        :raises ValueError: If capacity is not a positive integer.
        """
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.capacity = capacity
        self.cache = {}  # Maps key to DoublyLinkedListNode
        self.dll = DoublyLinkedList() # Manages the order of nodes

    def get(self, key: int) -> int:
        """
        Retrieves the value associated with the given key.
        If the key exists, its corresponding node is moved to the front of the DLL
        (most recently used).
        :param key: The key to retrieve.
        :return: The value associated with the key, or -1 if the key is not found.
        """
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self.dll.move_to_front(node) # Mark as recently used
        return node.value

    def put(self, key: int, value: int) -> None:
        """
        Inserts or updates a key-value pair in the cache.
        If the key already exists, its value is updated, and the node is moved
        to the front of the DLL.
        If the key does not exist:
            - If the cache is at capacity, the least recently used item (tail of DLL)
              is evicted.
            - A new node is created and added to the front of the DLL.
        :param key: The key to insert or update.
        :param value: The value to associate with the key.
        """
        if key in self.cache:
            node = self.cache[key]
            node.value = value  # Update the value of the existing node
            self.dll.move_to_front(node) # Mark as recently used/updated
        else:
            if self.dll.size >= self.capacity:
                # Evict LRU item (tail of DLL)
                lru_node = self.dll.remove_tail()
                if lru_node: # Ensure a node was actually removed
                    del self.cache[lru_node.key]

            new_node = DoublyLinkedListNode(key, value)
            self.dll.add_front(new_node)
            self.cache[key] = new_node
