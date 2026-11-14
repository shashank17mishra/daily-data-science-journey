"""Unit tests for SQL Schema Normalization (1NF to 3NF)."""

import sqlite3
import pytest
from learning.sql.day_075_schema_normalization import SchemaNormalizer


@pytest.fixture
def normalizer():
    """Fixture providing a seeded SchemaNormalizer instance."""
    norm = SchemaNormalizer(":memory:")
    norm.create_unnormalized_table()
    sample_data = [
        (
            101,
            "2026-03-01",
            1,
            "Alice Smith",
            "90210",
            "Beverly Hills",
            "CA",
            "1:Laptop:1200.0:1;2:Mouse:25.0:2",
        ),
        (
            102,
            "2026-03-02",
            2,
            "Bob Jones",
            "10001",
            "New York",
            "NY",
            "2:Mouse:25.0:1;3:Keyboard:75.0:1",
        ),
        (
            103,
            "2026-03-03",
            1,
            "Alice Smith",
            "90210",
            "Beverly Hills",
            "CA",
            "1:Laptop:1200.0:2",
        ),
    ]
    norm.seed_unnormalized_data(sample_data)
    yield norm
    norm.close()


def test_1nf_migration(normalizer):
    """Test that 1NF removes repeating CSV groups into atomic rows."""
    normalizer.migrate_to_1nf()
    rows = normalizer.execute_sql("SELECT * FROM orders_1nf ORDER BY order_id, item_id;")
    assert len(rows) == 5
    assert rows[0]["order_id"] == 101
    assert rows[0]["item_name"] == "Laptop"
    assert rows[0]["quantity"] == 1
    assert rows[1]["order_id"] == 101
    assert rows[1]["item_name"] == "Mouse"
    assert rows[1]["quantity"] == 2


def test_2nf_migration(normalizer):
    """Test that 2NF eliminates partial dependencies (item metadata moved to items_2nf)."""
    normalizer.migrate_to_1nf()
    normalizer.migrate_to_2nf()

    items = normalizer.execute_sql("SELECT * FROM items_2nf ORDER BY item_id;")
    assert len(items) == 3
    assert items[0] == {"item_id": 1, "item_name": "Laptop", "item_price": 1200.0}

    order_items = normalizer.execute_sql("SELECT * FROM order_items_2nf;")
    assert len(order_items) == 5


def test_3nf_migration(normalizer):
    """Test that 3NF eliminates transitive dependencies (Zip code -> City, State)."""
    normalizer.migrate_to_1nf()
    normalizer.migrate_to_2nf()
    normalizer.migrate_to_3nf()

    zips = normalizer.execute_sql("SELECT * FROM zip_locations_3nf ORDER BY zip_code;")
    assert len(zips) == 2
    assert zips[0] == {"zip_code": "10001", "city": "New York", "state": "NY"}
    assert zips[1] == {"zip_code": "90210", "city": "Beverly Hills", "state": "CA"}

    customers = normalizer.execute_sql("SELECT * FROM customers_3nf ORDER BY customer_id;")
    assert len(customers) == 2
    assert customers[0] == {"customer_id": 1, "customer_name": "Alice Smith", "zip_code": "90210"}

    orders = normalizer.execute_sql("SELECT * FROM orders_3nf ORDER BY order_id;")
    assert len(orders) == 3


def test_lossless_join_property(normalizer):
    """Verify that reconstructing 3NF tables via JOIN match 1NF atomic records."""
    normalizer.migrate_to_1nf()
    normalizer.migrate_to_2nf()
    normalizer.migrate_to_3nf()

    reconstructed = normalizer.reconstruct_3nf_to_flat()
    _1nf_rows = normalizer.execute_sql("SELECT * FROM orders_1nf ORDER BY order_id, item_id;")

    assert len(reconstructed) == len(_1nf_rows)
    for rec, orig in zip(reconstructed, _1nf_rows):
        assert rec["order_id"] == orig["order_id"]
        assert rec["customer_name"] == orig["customer_name"]
        assert rec["item_name"] == orig["item_name"]
        assert rec["quantity"] == orig["quantity"]


def test_referential_integrity_constraints(normalizer):
    """Verify FK constraints prevent invalid references in 3NF schema."""
    normalizer.migrate_to_1nf()
    normalizer.migrate_to_2nf()
    normalizer.migrate_to_3nf()

    with pytest.raises(sqlite3.IntegrityError):
        normalizer.conn.execute(
            "INSERT INTO customers_3nf (customer_id, customer_name, zip_code) VALUES (99, 'Eve', '00000');"
        )
