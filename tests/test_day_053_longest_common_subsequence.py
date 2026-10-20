"""
Unit tests for Day 053: DP Longest Common Subsequence.
"""

import pytest
from learning.dsa.day_053_longest_common_subsequence import LongestCommonSubsequence


class TestLongestCommonSubsequence:
    def test_lcs_length_basic(self):
        text1 = "AGGTAB"
        text2 = "GXTXAYB"
        assert LongestCommonSubsequence.lcs_length(text1, text2) == 4

    def test_lcs_length_empty(self):
        assert LongestCommonSubsequence.lcs_length("", "ABC") == 0
        assert LongestCommonSubsequence.lcs_length("ABC", "") == 0
        assert LongestCommonSubsequence.lcs_length("", "") == 0

    def test_lcs_length_no_common(self):
        assert LongestCommonSubsequence.lcs_length("ABC", "DEF") == 0

    def test_lcs_length_identical(self):
        assert LongestCommonSubsequence.lcs_length("PYTHON", "PYTHON") == 6

    def test_lcs_length_optimized_matches_standard(self):
        test_cases = [
            ("AGGTAB", "GXTXAYB"),
            ("ABCBDAB", "BDCABA"),
            ("AAAA", "AA"),
            ("DYNAMIC", "PROGRAMMING"),
            ("13456778", "241234145677"),
        ]
        for t1, t2 in test_cases:
            standard = LongestCommonSubsequence.lcs_length(t1, t2)
            optimized = LongestCommonSubsequence.lcs_length_optimized(t1, t2)
            assert standard == optimized

    def test_lcs_string_reconstruction(self):
        text1 = "AGGTAB"
        text2 = "GXTXAYB"
        lcs_str = LongestCommonSubsequence.get_one_lcs(text1, text2)
        assert lcs_str == "GTAB"
        assert len(lcs_str) == 4

    def test_all_lcs_strings_classic_example(self):
        text1 = "ABCBDAB"
        text2 = "BDCABA"
        all_lcs = LongestCommonSubsequence.get_all_lcs(text1, text2)
        expected = {"BCBA", "BCAB", "BDAB"}
        assert all_lcs == expected

    def test_all_lcs_strings_empty_cases(self):
        assert LongestCommonSubsequence.get_all_lcs("", "ABC") == {""}

    def test_all_lcs_strings_single_match(self):
        assert LongestCommonSubsequence.get_all_lcs("A", "A") == {"A"}

    @pytest.mark.parametrize(
        "s1, s2, expected_len",
        [
            ("XMJYAUZ", "MZJAWXU", 4),
            ("SHINCHAN", "NOHARAAA", 3),
            ("13456778", "241234145677", 7),
        ],
    )
    def test_lcs_parametrized(self, s1, s2, expected_len):
        assert LongestCommonSubsequence.lcs_length(s1, s2) == expected_len
