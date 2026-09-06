import pytest
from learning.python.day_005_exceptions import safe_parse_int, InvalidDataFormatError, ValueOutOfRangeError

def test_safe_parse_int_valid():
    assert safe_parse_int("42", 0, 100) == 42

def test_safe_parse_int_invalid_format():
    with pytest.raises(InvalidDataFormatError):
        safe_parse_int("abc")

def test_safe_parse_int_out_of_range():
    with pytest.raises(ValueOutOfRangeError):
        safe_parse_int("150", 0, 100)
