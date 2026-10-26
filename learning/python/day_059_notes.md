# Day 059: Substring Search (KMP Algorithm)

## Overview
Implementation of the Knuth-Morris-Pratt (KMP) string matching algorithm in Python, featuring LPS (Longest Prefix Suffix) array construction and efficient O(N + M) substring search supporting overlapping patterns, edge cases, and Unicode characters.

## Objectives
- Understand algorithmic mechanics of Substring Search (KMP Algorithm).
- Implement unit tests for edge cases.

## Key Concepts
The Knuth-Morris-Pratt (KMP) search algorithm improves naive substring searching from O(N * M) to linear time complexity O(N + M) by avoiding re-examination of previously matched characters. Key components include:

1. **Longest Prefix Suffix (LPS) Array**: Precomputes length of the longest proper prefix of pattern[0...i] that is also a suffix of pattern[0...i]. When a mismatch occurs, `lps[j-1]` dictates how many characters in the pattern can be skipped without stepping back in the text string.
2. **KMP Search Execution**: Uses two pointers (`i` for text, `j` for pattern). On character matches, both advance. On a mismatch, `j` fallback is determined by `lps[j-1]` while `i` continues forward, guaranteeing linear efficiency.
3. **Python Unicode Support**: Python 3 string indexing handles Unicode code points natively, ensuring character offsets match indexed search results reliably across single-byte and multi-byte characters.
