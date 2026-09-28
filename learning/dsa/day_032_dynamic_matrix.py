"""Dynamic Matrix with Dynamic Resizing and Efficient Submatrix Sum Queries.

This module provides a robust dynamic matrix class supporting core matrix
operations including resizing, rotation, transposition, and O(1) 2D region sum queries.
"""

from typing import List, Tuple, Union, Optional

Number = Union[int, float]


class DynamicMatrix:
    """A dynamic 2D numerical matrix supporting matrix transformations and 2D range sum queries."""

    def __init__(self, rows: int, cols: int, fill_value: Number = 0) -> None:
        """Initialize matrix with given dimensions and fill value.

        Args:
            rows: Number of rows (must be > 0).
            cols: Number of columns (must be > 0).
            fill_value: Initial default value for matrix elements.

        Raises:
            ValueError: If rows or cols are <= 0.
        """
        if rows <= 0 or cols <= 0:
            raise ValueError("Rows and columns must be positive integers.")

        self._rows = rows
        self._cols = cols
        self._grid: List[List[Number]] = [[fill_value] * cols for _ in range(rows)]
        self._prefix_sum: Optional[List[List[Number]]] = None

    @classmethod
    def from_list(cls, grid: List[List[Number]]) -> "DynamicMatrix":
        """Create a DynamicMatrix from a 2D list.

        Args:
            grid: Non-empty list of non-empty uniform-length lists of numbers.

        Returns:
            DynamicMatrix instance.

        Raises:
            ValueError: If grid is empty or rows have inconsistent lengths.
        """
        if not grid or not grid[0]:
            raise ValueError("Grid cannot be empty.")

        rows = len(grid)
        cols = len(grid[0])

        for row in grid:
            if len(row) != cols:
                raise ValueError("All rows in grid must have identical length.")

        instance = cls(rows, cols)
        instance._grid = [list(row) for row in grid]
        return instance

    @property
    def shape(self) -> Tuple[int, int]:
        """Return dimensions as (rows, cols)."""
        return self._rows, self._cols

    def get(self, row: int, col: int) -> Number:
        """Get element value at index (row, col)."""
        self._validate_bounds(row, col)
        return self._grid[row][col]

    def set(self, row: int, col: int, value: Number) -> None:
        """Set element value at index (row, col) and invalidate cached prefix sums."""
        self._validate_bounds(row, col)
        self._grid[row][col] = value
        self._prefix_sum = None

    def resize(self, new_rows: int, new_cols: int, fill_value: Number = 0) -> None:
        """Resize matrix to new dimensions.

        Extends rows/cols with fill_value or truncates if new dimensions are smaller.

        Args:
            new_rows: Target row count (> 0).
            new_cols: Target column count (> 0).
            fill_value: Value used when expanding matrix.
        """
        if new_rows <= 0 or new_cols <= 0:
            raise ValueError("New dimensions must be positive integers.")

        # Adjust columns for existing rows
        for r in range(min(self._rows, new_rows)):
            if new_cols > self._cols:
                self._grid[r].extend([fill_value] * (new_cols - self._cols))
            else:
                self._grid[r] = self._grid[r][:new_cols]

        # Adjust rows
        if new_rows > self._rows:
            for _ in range(new_rows - self._rows):
                self._grid.append([fill_value] * new_cols)
        else:
            self._grid = self._grid[:new_rows]

        self._rows = new_rows
        self._cols = new_cols
        self._prefix_sum = None

    def transpose(self) -> None:
        """Transpose matrix in-place (swap rows and columns)."""
        transposed = [
            [self._grid[r][c] for r in range(self._rows)]
            for c in range(self._cols)
        ]
        self._grid = transposed
        self._rows, self._cols = self._cols, self._rows
        self._prefix_sum = None

    def rotate(self, clockwise: bool = True) -> None:
        """Rotate matrix 90 degrees clockwise or counter-clockwise in-place."""
        if clockwise:
            self.transpose()
            for r in range(self._rows):
                self._grid[r].reverse()
        else:
            for r in range(self._rows):
                self._grid[r].reverse()
            self.transpose()
        self._prefix_sum = None

    def build_prefix_sum(self) -> None:
        """Build 2D prefix sum array for O(1) region sum queries."""
        pref = [[0] * (self._cols + 1) for _ in range(self._rows + 1)]

        for r in range(self._rows):
            for c in range(self._cols):
                pref[r + 1][c + 1] = (
                    self._grid[r][c]
                    + pref[r][c + 1]
                    + pref[r + 1][c]
                    - pref[r][c]
                )

        self._prefix_sum = pref

    def region_sum(self, r1: int, c1: int, r2: int, c2: int) -> Number:
        """Compute sum of elements in submatrix [r1..r2, c1..c2] inclusive in O(1) time.

        Args:
            r1: Top-left row index.
            c1: Top-left column index.
            r2: Bottom-right row index.
            c2: Bottom-right column index.

        Returns:
            Sum of values in designated region.
        """
        self._validate_bounds(r1, c1)
        self._validate_bounds(r2, c2)

        if r1 > r2 or c1 > c2:
            raise ValueError("Top-left indices must be <= bottom-right indices.")

        if self._prefix_sum is None:
            self.build_prefix_sum()

        P = self._prefix_sum
        return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]

    def to_list(self) -> List[List[Number]]:
        """Return deep copy of current matrix as 2D list."""
        return [list(row) for row in self._grid]

    def _validate_bounds(self, row: int, col: int) -> None:
        """Check if indices are within matrix boundary."""
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError(
                f"Index ({row}, {col}) out of bounds for matrix of shape {self.shape}."
            )
