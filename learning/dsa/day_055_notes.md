# Day 055: Advanced Trie (Prefix Tree)

## Overview
An advanced, full-featured Trie (Prefix Tree) implementation supporting insertion, exact search, prefix search, recursive deletion with branch pruning, wildcard pattern matching, prefix frequency counting, and auto-complete suggestions.

## Objectives
- Understand algorithmic mechanics of Trie (Prefix Tree).
- Implement unit tests for edge cases.

## Key Concepts
A Trie (Prefix Tree) is an $O(L)$ space/time optimization data structure (where $L$ is key length) for managing dynamic collections of strings. Key algorithmic mechanics:
1. **Tree Nodes**: Each `TrieNode` maintains a lookup map `children`, a boolean `is_end_of_word`, and a `prefix_count` tracking how many active words pass through that branch.
2. **Pruning Deletion**: During deletion, post-order recursive traversal decrements `prefix_count` along the path. If a child node has no remaining children and is not the terminus of another word, the parent's child reference is removed to reclaim space.
3. **Wildcard & Auto-complete**: Wildcard matching uses Depth First Search (DFS) to branch on '.' wildcard characters, while auto-completion navigates to the prefix sub-tree and collects terminal words lexicographically.
