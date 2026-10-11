# Day 045: Binary Search Tree (BST) Operations

## Overview
Implementation of a Binary Search Tree (BST) data structure supporting key operations: insertion, search, deletion across all structural cases (leaf node, single child, two children), standard tree traversals (in-order, pre-order, post-order), min/max queries, and structural validation.

## Objectives
- Understand algorithmic mechanics of Binary Search Tree (BST) Operations.
- Implement unit tests for edge cases.

## Key Concepts
### Binary Search Tree (BST) Operations & Mechanics

A Binary Search Tree (BST) is a hierarchical node-based data structure satisfying the following property for every node $N$:
- All values in $N$'s left subtree are strictly less than $N.val$.
- All values in $N$'s right subtree are strictly greater than $N.val$.

#### Key Algorithms & Time Complexity

1. **Search & Insert ($O(h)$ where $h$ is height)**:
   - Traverses left or right based on value comparison until target is found or an empty spot (`None`) is hit.
   - Average time complexity: $O(\log N)$ for balanced trees, worst-case: $O(N)$ for skewed trees.

2. **Deletion Cases ($O(h)$)**:
   - **Case 1 (Leaf Node)**: Directly remove reference from parent.
   - **Case 2 (Single Child)**: Replace target node reference with its only child.
   - **Case 3 (Two Children)**: Find the *in-order successor* (smallest node in right subtree), copy its value into the target node, and recursively delete the in-order successor.

3. **Traversals ($O(N)$)**:
   - **In-Order (Left, Root, Right)**: Yields elements in strictly sorted order.
   - **Pre-Order (Root, Left, Right)**: Useful for serialized cloning/copying of tree topology.
   - **Post-Order (Left, Right, Root)**: Useful for bottom-up node processing/deallocation.

4. **Validation ($O(N)$)**:
   - Validating a BST requires tracking global upper and lower bounds `(low, high)` during recursion down every sub-branch to ensure subtrees stay strictly bounded.
