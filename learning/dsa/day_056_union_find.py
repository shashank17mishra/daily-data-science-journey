"""
Disjoint-Set (Union-Find) Data Structure with Path Compression and Union by Rank.

This module provides a generic, efficient implementation of the Disjoint-Set
data structure supporting dynamic element registration, path compression,
union by rank, and component metadata queries.
"""

from typing import Generic, Hashable, TypeVar, Dict, List, Set, Optional

T = TypeVar("T", bound=Hashable)


class UnionFind(Generic[T]):
    """
    A Disjoint-Set Data Structure (Union-Find) with dynamic element addition,
    path compression, and union by rank optimizations.
    """

    def __init__(self, elements: Optional[List[T]] = None) -> None:
        """
        Initialize Union-Find with an optional iterable of elements.

        Args:
            elements: Initial collection of hashable elements.
        """
        self._parent: Dict[T, T] = {}
        self._rank: Dict[T, int] = {}
        self._size: Dict[T, int] = {}
        self._num_components: int = 0

        if elements is not None:
            for elem in elements:
                self.add(elem)

    @property
    def num_components(self) -> int:
        """Return the total number of disjoint sets currently tracked."""
        return self._num_components

    def __len__(self) -> int:
        """Return total number of tracked elements across all sets."""
        return len(self._parent)

    def __contains__(self, element: T) -> bool:
        """Check if an element is tracked by the UnionFind data structure."""
        return element in self._parent

    def add(self, element: T) -> bool:
        """
        Add a new element into its own isolated set.

        Args:
            element: Hashable item to track.

        Returns:
            bool: True if element was newly added, False if already present.
        """
        if element in self._parent:
            return False

        self._parent[element] = element
        self._rank[element] = 0
        self._size[element] = 1
        self._num_components += 1
        return True

    def find(self, element: T) -> T:
        """
        Find the representative (root) of the set containing `element`.
        Applies iterative path compression during traversal.

        Args:
            element: Element whose representative is queried.

        Returns:
            The representative element of the set.

        Raises:
            KeyError: If the element is not tracked in the data structure.
        """
        if element not in self._parent:
            raise KeyError(f"Element {element!r} is not present in UnionFind.")

        root = element
        while root != self._parent[root]:
            root = self._parent[root]

        curr = element
        while curr != root:
            nxt = self._parent[curr]
            self._parent[curr] = root
            curr = nxt

        return root

    def union(self, x: T, y: T) -> bool:
        """
        Unify the set containing `x` and the set containing `y` using rank.

        Args:
            x: First element.
            y: Second element.

        Returns:
            bool: True if sets were merged, False if already in the same set.
        """
        if x not in self._parent:
            self.add(x)
        if y not in self._parent:
            self.add(y)

        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self._rank[root_x] < self._rank[root_y]:
            root_x, root_y = root_y, root_x

        self._parent[root_y] = root_x
        self._size[root_x] += self._size[root_y]

        if self._rank[root_x] == self._rank[root_y]:
            self._rank[root_x] += 1

        self._num_components -= 1
        return True

    def connected(self, x: T, y: T) -> bool:
        """
        Check whether `x` and `y` belong to the same connected component.

        Args:
            x: First element.
            y: Second element.

        Returns:
            bool: True if connected, False otherwise.
        """
        if x not in self._parent or y not in self._parent:
            return False
        return self.find(x) == self.find(y)

    def get_component_size(self, element: T) -> int:
        """
        Get size of the set containing `element`.

        Args:
            element: Element to query.

        Returns:
            int: Number of elements in the element's set.

        Raises:
            KeyError: If element is not tracked.
        """
        root = self.find(element)
        return self._size[root]

    def get_components(self) -> Dict[T, Set[T]]:
        """
        Group all elements by their set representative.

        Returns:
            Dict mapping root element -> Set of all elements in that set.
        """
        components: Dict[T, Set[T]] = {}
        for elem in self._parent:
            root = self.find(elem)
            if root not in components:
                components[root] = set()
            components[root].add(elem)
        return components
