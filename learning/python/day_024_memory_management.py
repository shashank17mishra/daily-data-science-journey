"""
Day 024: Memory Management & Garbage Collection
Practical implementation of reference counting, cycle detection, weak references, and safe finalizers.
"""

import gc
import sys
import weakref
from typing import Any, Dict, Optional, Set


def get_ref_count(obj: Any) -> int:
    """
    Returns the reference count of an object using sys.getrefcount.
    
    Note: CPython's sys.getrefcount(obj) includes the temporary reference
    created by passing obj as an argument to the function. Reference count
    testing should therefore verify relative deltas when references are added
    or removed.
    """
    return sys.getrefcount(obj)


class Node:
    """Graph node used for demonstrating and testing circular reference cycles."""

    def __init__(self, name: str):
        self.name = name
        self.peer: Optional["Node"] = None

    def link(self, other: "Node") -> None:
        """Creates a circular reference between this node and another."""
        self.peer = other
        other.peer = self


def cleanup_circular_references() -> int:
    """
    Forces a garbage collection sweep to detect and free cyclic garbage.
    Returns the number of unreachable objects collected.
    """
    return gc.collect()


class WeakCache:
    """
    Cache utilizing weak references to allow cached objects to be
    garbage-collected when no longer referenced externally.
    """

    def __init__(self):
        self._cache: weakref.WeakValueDictionary = weakref.WeakValueDictionary()

    def set(self, key: str, value: Any) -> None:
        """Stores an object in cache via weak reference."""
        self._cache[key] = value

    def get(self, key: str) -> Optional[Any]:
        """Retrieves an object if still alive, else None."""
        return self._cache.get(key, None)

    def contains(self, key: str) -> bool:
        """Checks if key is present and still referenced."""
        return key in self._cache

    def __len__(self) -> int:
        return len(self._cache)


class ResourceTracker:
    """
    Tracks external resources using weakref.finalize for reliable teardown.
    
    IMPORTANT: The finalizer callback is a static method to avoid binding
    `self`, which would otherwise create a strong reference preventing
    the instance from ever being collected.
    """

    _active_resources: Dict[str, Dict[str, Any]] = {}

    def __init__(self, resource_id: str):
        self.resource_id = resource_id
        ResourceTracker._active_resources[resource_id] = {
            "status": "open",
            "closed_via": None,
        }
        # Unbound callback ensures no cycle to self
        self._finalizer = weakref.finalize(
            self,
            ResourceTracker._teardown_callback,
            resource_id,
            ResourceTracker._active_resources,
            "gc",
        )

    @staticmethod
    def _teardown_callback(resource_id: str, registry: Dict[str, Any], method: str) -> None:
        """Teardown callback executed either explicitly or upon GC collection."""
        if resource_id in registry:
            registry[resource_id]["status"] = "closed"
            registry[resource_id]["closed_via"] = method

    def close(self) -> None:
        """Explicitly release the resource before GC."""
        if self._finalizer.alive:
            # Update registry status and invoke finalizer
            ResourceTracker._teardown_callback(
                self.resource_id, ResourceTracker._active_resources, "explicit"
            )
            self._finalizer.detach()

    @property
    def is_alive(self) -> bool:
        """Returns True if the finalizer is still active and object not yet collected/closed."""
        return self._finalizer.alive

    @classmethod
    def get_resource_status(cls, resource_id: str) -> Optional[Dict[str, Any]]:
        """Returns state of the tracked resource."""
        return cls._active_resources.get(resource_id)

    @classmethod
    def clear_registry(cls) -> None:
        """Clears all active resource tracking records."""
        cls._active_resources.clear()


def get_deep_size(obj: Any, seen: Optional[Set[int]] = None) -> int:
    """
    Recursively calculates the deep memory footprint of an object in bytes.
    Handles cyclic structures by tracking visited object IDs.
    """
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)

    size = sys.getsizeof(obj)

    if isinstance(obj, dict):
        size += sum(get_deep_size(k, seen) + get_deep_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(get_deep_size(item, seen) for item in obj)

    return size
