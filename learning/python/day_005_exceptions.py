"""
Day 005: Robust Exception Handling and Custom Exception Hierarchy.
"""
class InvalidDataFormatError(Exception):
    """Raised when data format validation fails."""
    pass

class ValueOutOfRangeError(ValueError):
    """Raised when a numerical value is outside acceptable range."""
    pass

def safe_parse_int(value: str, min_val: int = 0, max_val: int = 100) -> int:
    """Parses a string integer, validating numeric boundaries safely."""
    try:
        parsed = int(value)
    except (ValueError, TypeError) as e:
        raise InvalidDataFormatError(f"Cannot convert '{value}' to integer.") from e

    if not (min_val <= parsed <= max_val):
        raise ValueOutOfRangeError(f"Parsed value {parsed} is out of bounds [{min_val}, {max_val}].")

    return parsed
