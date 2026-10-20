# Day 053: DP: Longest Common Subsequence

## Overview
Implementation of Longest Common Subsequence (LCS) algorithms usingDynamic Programming, featuring standard 2D DP, space-optimized 1D DP, standard back-tracking string reconstruction, and complete extraction of all distinct longest common subsequences.

## Objectives
- Understand dynamic programming recurrence relations for sequence alignment and LCS.
- Implement space optimization techniques reducing memory complexity from O(m*n) to O(min(m, n)).
- Reconstruct single and all distinct longest common subsequence strings using DP table backtracking.
- Implement robust unit tests covering edge cases like empty strings, non-overlapping sequences, identical sequences, and multi-subsequence extractions.

## Key Concepts
Longest Common Subsequence (LCS) is a fundamental problem in dynamic programming.

Recurrence Relation:
Let DP[i][j] be the length of the LCS of prefixes text1[0..i-1] and text2[0..j-1]:
- If text1[i-1] == text2[j-1]: DP[i][j] = DP[i-1][j-1] + 1
- Else: DP[i][j] = max(DP[i-1][j], DP[i][j-1])

Space Optimization:
Notice that DP[i][j] only depends on the current and previous rows (DP[i-1]). Thus, we can optimize space from O(m*n) to O(min(m, n)) by keeping a 1D array and a single temporary scalar variable (`prev`).

String Reconstruction:
- To reconstruct one LCS: backtrack from DP[m][n] towards DP[0][0].
- To reconstruct all distinct LCS strings: backtrack recursively from DP[m][n] with memoization, branching when DP[i-1][j] == DP[i][j-1] to gather all unique valid paths.
