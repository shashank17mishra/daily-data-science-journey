import pytest
from learning.python.day_001_variables import inspect_variable_types, calculate_bmi

def test_inspect_variable_types():
    res = inspect_variable_types("Alice", 25, 1.68, True)
    assert res["name"] == ("Alice", "str")
    assert res["age"] == (25, "int")
    assert res["height_m"] == (1.68, "float")
    assert res["is_student"] == (True, "bool")

def test_calculate_bmi():
    bmi = calculate_bmi(70, 1.75)
    assert bmi == 22.86

def test_calculate_bmi_invalid():
    with pytest.raises(ValueError):
        calculate_bmi(70, 0)
