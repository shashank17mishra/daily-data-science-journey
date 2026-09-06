"""
Day 002: Functions, Positional/Keyword Arguments, and Variadic Parameters (*args, **kwargs).
"""
from typing import List, Dict, Any, Union

def calculate_summary_stats(*args: Union[int, float], **kwargs: Any) -> Dict[str, Any]:
    """Calculates min, max, mean of numeric positional args and attaches metadata from kwargs."""
    if not args:
        raise ValueError("At least one numerical argument must be provided.")

    numeric_values = [float(val) for val in args]
    summary = {
        "count": len(numeric_values),
        "min": min(numeric_values),
        "max": max(numeric_values),
        "mean": sum(numeric_values) / len(numeric_values)
    }

    for k, v in kwargs.items():
        summary[k] = v

    return summary
