# Day 027: Shallow vs Deep Copying

## Overview
An advanced exploration of shallow vs deep copying in Python. This exercise implements a custom GraphNode class that demonstrates how to customize copying behavior using __copy__ and __deepcopy__, specifically handling cyclic references to prevent infinite recursion.

## Objectives
- Understand the fundamental difference between shallow and deep copying.
- Implement custom copying behavior using __copy__ and __deepcopy__ magic methods.
- Handle cyclic references correctly in custom deepcopy implementations using the memo dictionary.

## Key Concepts
In Python, assignment statements do not copy objects; they only bind names to objects. For collections or custom objects containing other objects, we often need to create copies. A shallow copy constructs a new compound object and then inserts references into it to the objects found in the original. A deep copy constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original. When implementing custom classes, we can override this behavior using `__copy__` and `__deepcopy__`. For deep copies of complex structures like graphs, handling cyclic references is critical. The `__deepcopy__` method accepts a `memo` dictionary which maps original object IDs to their newly copied counterparts, preventing infinite recursion and preserving the graph's topology.
