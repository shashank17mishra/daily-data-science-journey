"""
Day 004: Pythonic List, Set, and Dictionary Comprehensions.
"""
from typing import List, Dict

def filter_even_squares(numbers: List[int]) -> List[int]:
    """Uses list comprehension to square even numbers from input list."""
    return [n ** 2 for n in numbers if n % 2 == 0]

def build_grade_map(scores: Dict[str, float]) -> Dict[str, str]:
    """Uses dictionary comprehension to map student names to Letter Grades."""
    return {
        name: ("Pass" if score >= 60 else "Fail")
        for name, score in scores.items()
    }
