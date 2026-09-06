"""
Day 001: Python Variables and Basic Data Types
Demonstrates dynamic typing, numeric operations, string manipulations, and type conversions.
"""

def inspect_variable_types(name: str, age: int, height_m: float, is_student: bool) -> dict:
    """Returns a dictionary containing variable values and their Python type names."""
    return {
        "name": (name, type(name).__name__),
        "age": (age, type(age).__name__),
        "height_m": (height_m, type(height_m).__name__),
        "is_student": (is_student, type(is_student).__name__)
    }

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculates Body Mass Index given weight in kg and height in meters."""
    if height_m <= 0:
        raise ValueError("Height must be strictly positive.")
    return round(weight_kg / (height_m ** 2), 2)
