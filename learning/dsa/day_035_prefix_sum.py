from typing import List, Union

class PrefixSum1D:
    """
    Implements a 1D Prefix Sum Array to answer range sum queries in O(1) time.
    """
    def __init__(self, arr: List[Union[int, float]]):
        self.arr = arr
        self.prefix = [0] * (len(arr) + 1)
        for i in range(len(arr)):
            self.prefix[i + 1] = self.prefix[i] + arr[i]

    def query(self, left: int, right: int) -> Union[int, float]:
        """
        Returns the sum of elements from index left to right (inclusive).
        Complexity: O(1)
        """
        if not self.arr:
            raise ValueError("Cannot query an empty array.")
        if left < 0 or right >= len(self.arr):
            raise IndexError("Query indices out of bounds.")
        if left > right:
            raise ValueError("Left index must be less than or equal to right index.")
        return self.prefix[right + 1] - self.prefix[left]


class PrefixSum2D:
    """
    Implements a 2D Prefix Sum Array (Summed-Area Table) to answer subgrid sum queries in O(1) time.
    """
    def __init__(self, matrix: List[List[Union[int, float]]]):
        if not matrix or not matrix[0]:
            self.matrix = []
            self.prefix = []
            return
        
        self.matrix = matrix
        R, C = len(matrix), len(matrix[0])
        self.prefix = [[0] * (C + 1) for _ in range(R + 1)]
        
        for r in range(R):
            for c in range(C):
                self.prefix[r + 1][c + 1] = (
                    matrix[r][c]
                    + self.prefix[r][c + 1]
                    + self.prefix[r + 1][c]
                    - self.prefix[r][c]
                )

    def query(self, r1: int, c1: int, r2: int, c2: int) -> Union[int, float]:
        """
        Returns the sum of the subgrid from (r1, c1) to (r2, c2) inclusive.
        Complexity: O(1)
        """
        if not self.matrix:
            raise ValueError("Cannot query an empty matrix.")
        
        R, C = len(self.matrix), len(self.matrix[0])
        if not (0 <= r1 <= r2 < R) or not (0 <= c1 <= c2 < C):
            raise IndexError("Query coordinates out of bounds or invalid range.")
            
        return (
            self.prefix[r2 + 1][c2 + 1]
            - self.prefix[r1][c2 + 1]
            - self.prefix[r2 + 1][c1]
            + self.prefix[r1][c1]
        )
