"""
Day 003: Lists, Tuples, Sets, and Dictionaries operations.
"""
from typing import List, Set, Dict, Tuple

def deduplicate_and_sort(items: List[int]) -> List[int]:
    """Removes duplicate elements using set operations and returns a sorted list."""
    return sorted(list(set(items)))

def find_common_skills(user1_skills: Set[str], user2_skills: Set[str]) -> Set[str]:
    """Returns set intersection of skills shared by both users."""
    return user1_skills.intersection(user2_skills)

def count_word_frequencies(text: str) -> Dict[str, int]:
    """Counts frequency of unique lowercase words in a string."""
    words = text.lower().strip().split()
    counts = {}
    for word in words:
        clean_word = word.strip(".,!?\"'")
        if clean_word:
            counts[clean_word] = counts.get(clean_word, 0) + 1
    return counts
