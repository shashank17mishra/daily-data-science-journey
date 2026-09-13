"""Day 016: Dataclasses & Structured Data implementation.

This module demonstrates modern usage of Python dataclasses including default factories,
post-initialization validation, immutability, and dict/tuple conversion utilities.
"""

from dataclasses import dataclass, field, asdict, astuple
from typing import List, Dict, Any
import uuid


@dataclass(frozen=True)
class Product:
    """Immutable product representation."""
    sku: str
    name: str
    unit_price: float

    def __post_init__(self) -> None:
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative.")


@dataclass
class InventoryItem:
    """Mutable inventory item with calculated total value and default metadata."""
    product: Product
    quantity: int = 0
    tags: List[str] = field(default_factory=list)
    item_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative.")

    @property
    def total_value(self) -> float:
        """Calculate total monetary value of this inventory item."""
        return round(self.product.unit_price * self.quantity, 2)

    def add_tag(self, tag: str) -> None:
        """Add a unique tag to the inventory item."""
        cleaned_tag = tag.strip().lower()
        if cleaned_tag and cleaned_tag not in self.tags:
            self.tags.append(cleaned_tag)

    def to_dict(self) -> Dict[str, Any]:
        """Convert dataclass instance to dictionary."""
        data = asdict(self)
        data["total_value"] = self.total_value
        return data
