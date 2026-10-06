"""Singly Linked List Data Structure and Operations."""

from typing import Any, List, Optional


class Node:
    """A node in a singly linked list."""

    def __init__(self, value: Any, next_node: Optional["Node"] = None) -> None:
        self.value = value
        self.next = next_node

    def __repr__(self) -> str:
        return f"Node({self.value!r})"


class SinglyLinkedList:
    """Implementation of a Singly Linked List with common operations."""

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        """Check if the linked list is empty."""
        return self.head is None

    def append(self, value: Any) -> None:
        """Add a new node with value to the end of the list."""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def prepend(self, value: Any) -> None:
        """Add a new node with value to the start of the list."""
        new_node = Node(value, next_node=self.head)
        self.head = new_node
        self._size += 1

    def insert_at(self, index: int, value: Any) -> None:
        """Insert a value at a specific index."""
        if index < 0 or index > self._size:
            raise IndexError("Index out of bounds")

        if index == 0:
            self.prepend(value)
            return

        current = self.head
        for _ in range(index - 1):
            assert current is not None
            current = current.next

        assert current is not None
        new_node = Node(value, next_node=current.next)
        current.next = new_node
        self._size += 1

    def delete_value(self, value: Any) -> bool:
        """Delete the first node containing the given value. Returns True if found and deleted."""
        if self.head is None:
            return False

        if self.head.value == value:
            self.head = self.head.next
            self._size -= 1
            return True

        current = self.head
        while current.next is not None and current.next.value != value:
            current = current.next

        if current.next is not None:
            current.next = current.next.next
            self._size -= 1
            return True

        return False

    def delete_at(self, index: int) -> Any:
        """Delete and return the value at the specified index."""
        if index < 0 or index >= self._size or self.head is None:
            raise IndexError("Index out of bounds")

        if index == 0:
            val = self.head.value
            self.head = self.head.next
            self._size -= 1
            return val

        current = self.head
        for _ in range(index - 1):
            assert current is not None
            current = current.next

        assert current is not None and current.next is not None
        val = current.next.value
        current.next = current.next.next
        self._size -= 1
        return val

    def find(self, value: Any) -> int:
        """Find the index of the first occurrence of value. Returns -1 if not found."""
        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def reverse(self) -> None:
        """Reverse the linked list in-place."""
        prev = None
        current = self.head
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def to_list(self) -> List[Any]:
        """Convert the linked list into a standard Python list."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result
