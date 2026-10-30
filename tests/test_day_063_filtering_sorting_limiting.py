"""
Unit tests for SQL Filtering, Sorting, and Limiting implementation.
"""

import pytest
from learning.sql.day_063_filtering_sorting_limiting import ProductRepository


@pytest.fixture
def repo():
    """Fixture providing an initialized in-memory database with seeded products."""
    repository = ProductRepository(":memory:")
    sample_data = [
        {"name": "Laptop", "category": "Electronics", "price": 1200.0, "stock": 10},
        {"name": "Smartphone", "category": "Electronics", "price": 800.0, "stock": 25},
        {"name": "Headphones", "category": "Electronics", "price": 150.0, "stock": 50},
        {"name": "Desk Chair", "category": "Furniture", "price": 200.0, "stock": 15},
        {"name": "Dining Table", "category": "Furniture", "price": 500.0, "stock": 5},
        {"name": "Monitor", "category": "Electronics", "price": 300.0, "stock": 20},
        {"name": "Bookshelf", "category": "Furniture", "price": 120.0, "stock": 8},
        {"name": "Coffee Maker", "category": "Appliances", "price": 90.0, "stock": 30},
        {"name": "Blender", "category": "Appliances", "price": 60.0, "stock": 40},
        {"name": "Microwave", "category": "Appliances", "price": 110.0, "stock": 12},
    ]
    repository.seed_products(sample_data)
    yield repository
    repository.close()


def test_seed_and_count(repo):
    results = repo.filter_products()
    assert len(results) == 10


def test_filter_by_category(repo):
    electronics = repo.filter_products(category="Electronics")
    assert len(electronics) == 4
    for row in electronics:
        assert row["category"] == "Electronics"


def test_filter_by_price_range(repo):
    affordable = repo.filter_products(min_price=100.0, max_price=300.0)
    assert len(affordable) == 5
    prices = [row["price"] for row in affordable]
    assert all(100.0 <= p <= 300.0 for p in prices)


def test_get_sorted_products(repo):
    sorted_asc = repo.get_sorted_products(sort_by="price", order="ASC")
    prices_asc = [row["price"] for row in sorted_asc]
    assert prices_asc == sorted(prices_asc)
    assert prices_asc[0] == 60.0

    sorted_desc = repo.get_sorted_products(sort_by="price", order="DESC")
    prices_desc = [row["price"] for row in sorted_desc]
    assert prices_desc == sorted(prices_desc, reverse=True)
    assert prices_desc[0] == 1200.0


def test_invalid_sort_parameters(repo):
    with pytest.raises(ValueError, match="Invalid sort column"):
        repo.get_sorted_products(sort_by="non_existent_column")

    with pytest.raises(ValueError, match="Invalid sort order"):
        repo.get_sorted_products(sort_by="price", order="INVALID")


def test_get_paginated_products(repo):
    page_1 = repo.get_paginated_products(limit=3, offset=0, sort_by="price", order="ASC")
    assert len(page_1) == 3
    assert page_1[0]["price"] == 60.0

    page_2 = repo.get_paginated_products(limit=3, offset=3, sort_by="price", order="ASC")
    assert len(page_2) == 3
    assert page_2[0]["price"] > page_1[-1]["price"]


def test_paginated_with_category_filter(repo):
    electronics_top2 = repo.get_paginated_products(
        limit=2, offset=0, category="Electronics", sort_by="price", order="DESC"
    )
    assert len(electronics_top2) == 2
    assert electronics_top2[0]["name"] == "Laptop"
    assert electronics_top2[1]["name"] == "Smartphone"
