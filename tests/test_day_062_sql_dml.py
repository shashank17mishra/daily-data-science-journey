import pytest
from learning.sql.day_062_sql_dml import InventoryRepository


@pytest.fixture
def repo():
    """Fixture providing an in-memory inventory repository."""
    repository = InventoryRepository(db_path=":memory:")
    yield repository
    repository.close()


def test_insert_product(repo):
    item_id = repo.insert_product("Laptop", "Electronics", 999.99, 10)
    assert item_id == 1

    product = repo.get_product(item_id)
    assert product is not None
    assert product["name"] == "Laptop"
    assert product["category"] == "Electronics"
    assert product["price"] == 999.99
    assert product["stock"] == 10


def test_bulk_insert_products(repo):
    products = [
        ("Mouse", "Electronics", 25.50, 50),
        ("Keyboard", "Electronics", 75.00, 30),
        ("Desk Chair", "Furniture", 150.00, 5),
    ]
    inserted_count = repo.bulk_insert_products(products)
    assert inserted_count == 3

    all_products = repo.get_all_products()
    assert len(all_products) == 3
    assert all_products[0]["name"] == "Mouse"
    assert all_products[2]["category"] == "Furniture"


def test_update_product_price(repo):
    item_id = repo.insert_product("Monitor", "Electronics", 200.00, 15)
    updated = repo.update_product_price(item_id, 220.00)
    assert updated is True

    product = repo.get_product(item_id)
    assert product["price"] == 220.00

    # Updating non-existent product
    assert repo.update_product_price(999, 100.00) is False


def test_bulk_update_category_prices(repo):
    products = [
        ("Mouse", "Electronics", 100.00, 10),
        ("Keyboard", "Electronics", 200.00, 10),
        ("Desk", "Furniture", 300.00, 5),
    ]
    repo.bulk_insert_products(products)

    updated_count = repo.bulk_update_category_prices("Electronics", 10.0)
    assert updated_count == 2

    elec_mouse = repo.get_product(1)
    elec_kbd = repo.get_product(2)
    furniture = repo.get_product(3)

    assert elec_mouse["price"] == 110.00
    assert elec_kbd["price"] == 220.00
    assert furniture["price"] == 300.00


def test_update_stock(repo):
    item_id = repo.insert_product("Phone", "Electronics", 500.00, 10)

    # Valid reduction
    assert repo.update_stock(item_id, -3) is True
    assert repo.get_product(item_id)["stock"] == 7

    # Valid addition
    assert repo.update_stock(item_id, 5) is True
    assert repo.get_product(item_id)["stock"] == 12

    # Invalid reduction exceeding available stock
    assert repo.update_stock(item_id, -20) is False
    assert repo.get_product(item_id)["stock"] == 12


def test_delete_product(repo):
    item_id = repo.insert_product("Tablet", "Electronics", 300.00, 8)
    assert repo.get_product(item_id) is not None

    deleted = repo.delete_product(item_id)
    assert deleted is True
    assert repo.get_product(item_id) is None

    # Deleting already deleted item
    assert repo.delete_product(item_id) is False


def test_delete_out_of_stock(repo):
    products = [
        ("Item A", "General", 10.0, 0),
        ("Item B", "General", 20.0, 5),
        ("Item C", "General", 30.0, 0),
    ]
    repo.bulk_insert_products(products)

    deleted_count = repo.delete_out_of_stock()
    assert deleted_count == 2

    remaining = repo.get_all_products()
    assert len(remaining) == 1
    assert remaining[0]["name"] == "Item B"
