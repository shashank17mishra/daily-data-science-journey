"""
Day 007: Object-Oriented Programming (Classes, Inheritance, Encapsulation, Methods).
"""
class Dataset:
    """Base class representing a dataset."""
    def __init__(self, name: str, data: list):
        self.name = name
        self._data = list(data)  # Encapsulated attribute

    @property
    def size(self) -> int:
        """Returns the number of elements in dataset."""
        return len(self._data)

    def summary(self) -> str:
        """Returns basic summary string."""
        return f"Dataset '{self.name}' containing {self.size} items."

class NumericDataset(Dataset):
    """Subclass specialized for numerical datasets."""
    def mean(self) -> float:
        """Calculates mean value of numeric elements."""
        if not self._data:
            raise ValueError("Cannot calculate mean of empty dataset.")
        return sum(self._data) / len(self._data)
