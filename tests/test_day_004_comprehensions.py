from learning.python.day_004_comprehensions import filter_even_squares, build_grade_map

def test_filter_even_squares():
    assert filter_even_squares([1, 2, 3, 4, 5, 6]) == [4, 16, 36]

def test_build_grade_map():
    scores = {"Alice": 85.0, "Bob": 45.0, "Charlie": 60.0}
    assert build_grade_map(scores) == {"Alice": "Pass", "Bob": "Fail", "Charlie": "Pass"}
