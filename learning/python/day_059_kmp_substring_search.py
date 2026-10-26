"""Knuth-Morris-Pratt (KMP) Substring Search Algorithm.

This module provides an efficient implementation of the KMP pattern searching algorithm,
which searches for occurrences of a pattern within a text string in O(N + M) time complexity.
"""

from typing import List


def compute_lps_array(pattern: str) -> List[int]:
    """Compute the Longest Prefix Suffix (LPS) array for the pattern.

    LPS[i] stores the length of the longest proper prefix of pattern[0...i]
    that is also a suffix of pattern[0...i].

    Args:
        pattern: The pattern string to analyze.

    Returns:
        A list of integers representing the LPS array.
    """
    if not pattern:
        return []

    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str) -> List[int]:
    """Find all starting 0-based index positions of pattern in text using KMP search.

    Args:
        text: The main text string to search within.
        pattern: The substring pattern to search for.

    Returns:
        A list of starting index positions where the pattern occurs in text.
    """
    if not pattern or not text or len(pattern) > len(text):
        return []

    lps = compute_lps_array(pattern)
    matches: List[int] = []

    i = 0  # Index for text
    j = 0  # Index for pattern

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == len(pattern):
            matches.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches


def kmp_contains(text: str, pattern: str) -> bool:
    """Check if pattern exists within text using KMP search.

    Args:
        text: The main text string.
        pattern: The pattern string.

    Returns:
        True if pattern is found, False otherwise.
    """
    if not pattern:
        return False
    return len(kmp_search(text, pattern)) > 0
