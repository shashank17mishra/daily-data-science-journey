from learning.python.day_003_data_structures import deduplicate_and_sort, find_common_skills, count_word_frequencies

def test_deduplicate_and_sort():
    assert deduplicate_and_sort([4, 2, 2, 8, 4, 1]) == [1, 2, 4, 8]

def test_find_common_skills():
    s1 = {"python", "sql", "git"}
    s2 = {"sql", "docker", "python"}
    assert find_common_skills(s1, s2) == {"python", "sql"}

def test_count_word_frequencies():
    text = "Data Science is great! Python for Data Science."
    counts = count_word_frequencies(text)
    assert counts["data"] == 2
    assert counts["science"] == 2
    assert counts["python"] == 1
