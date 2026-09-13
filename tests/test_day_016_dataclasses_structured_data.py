"""Unit tests for Day 016 Dataclasses implementation."""

import pytest
from dataclasses import FrozenInstanceError
from learning.python.day_016_dataclasses_structured_data import Product, InventoryItem


def test_product_creation_and_immutability():
    prod = Product(sku="PROD-001", name="Widget", unit_price=19.99)
    assert prod.sku == "PROD-001"
    assert prod.name == "Widget"
    assert prod.unit_price == 19.99

    with pytest.raises(FrozenInstanceError):
        prod.unit_price = 25.00


def test_product_validation():
    with pytest.raises(ValueError, match="Unit price cannot be negative."):
        Product(sku="PROD-002", name="Invalid Widget", unit_price=-5.00)


def test_inventory_item_defaults_and_calculation():
    prod = Product(sku="PROD-003", name="Gadget", unit_price=10.50)
    item = InventoryItem(product=prod, quantity=4)

    assert item.quantity == 4
    assert item.tags == []
    assert len(item.item_id) > 0
    assert item.total_value == 42.00


def test_inventory_item_mutable_operations():
    prod = Product(sku="PROD-004", name="Tool", unit_price=5.00)
    item = InventoryItem(product=prod, quantity=2)

    item.add_tag("Hardware")
    item.add_tag(" hardware ")
    assert item.tags == ["hardware"]


def test_inventory_item_to_dict():
    prod = Product(sku="PROD-005", name="Bolt", unit_price=0.50)
    item = InventoryItem(product=prod, quantity=100, tags=["fastener"])
    dict_repr = item.to_dict()

    assert dict_repr["product"]["sku"] == "PROD-005"
    assert dict_repr["quantity"] == 100
    assert dict_repr["tags"] == ["fastener"]
    assert dict_repr["total_value"] == 50.00
