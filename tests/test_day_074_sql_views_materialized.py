import time
import pytest
from learning.sql.day_074_sql_views_materialized import SQLViewManager


@pytest.fixture
def db_manager():
    manager = SQLViewManager(":memory:")
    manager.setup_schema()
    manager.insert_product(1, "Laptop", "Electronics", 1200.0)
    manager.insert_product(2, "Phone", "Electronics", 800.0)
    manager.insert_product(3, "Desk", "Furniture", 300.0)

    manager.insert_order(101, 1, 1, 2, "2026-03-01")
    manager.insert_order(102, 2, 2, 1, "2026-03-02")
    manager.insert_order(103, 1, 3, 4, "2026-03-03")
    yield manager
    manager.close()


def test_standard_view_dynamic_update(db_manager):
    query = """
    SELECT p.category, SUM(o.quantity * p.price) as total_sales
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category
    """
    db_manager.create_standard_view("v_sales_by_category", query)

    res = db_manager.fetch_all("SELECT * FROM v_sales_by_category WHERE category = 'Electronics'")
    assert len(res) == 1
    assert res[0]["total_sales"] == (2 * 1200.0 + 1 * 800.0)

    db_manager.insert_order(104, 3, 2, 2, "2026-03-04")
    res_updated = db_manager.fetch_all("SELECT * FROM v_sales_by_category WHERE category = 'Electronics'")
    assert res_updated[0]["total_sales"] == (2 * 1200.0 + 1 * 800.0 + 2 * 800.0)


def test_materialized_view_staleness_and_refresh(db_manager):
    query = """
    SELECT p.category, SUM(o.quantity * p.price) as total_sales
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category
    """
    db_manager.create_materialized_view("mv_sales_by_category", query)

    assert not db_manager.is_materialized_view_stale("mv_sales_by_category", ["orders", "products"])

    initial_res = db_manager.fetch_all("SELECT * FROM mv_sales_by_category WHERE category = 'Furniture'")
    assert initial_res[0]["total_sales"] == (4 * 300.0)

    time.sleep(0.01)

    db_manager.insert_order(105, 1, 3, 1, "2026-03-05")

    mv_res_before = db_manager.fetch_all("SELECT * FROM mv_sales_by_category WHERE category = 'Furniture'")
    assert mv_res_before[0]["total_sales"] == (4 * 300.0)
    assert db_manager.is_materialized_view_stale("mv_sales_by_category", ["orders", "products"])

    db_manager.refresh_materialized_view("mv_sales_by_category")

    mv_res_after = db_manager.fetch_all("SELECT * FROM mv_sales_by_category WHERE category = 'Furniture'")
    assert mv_res_after[0]["total_sales"] == (5 * 300.0)
    assert not db_manager.is_materialized_view_stale("mv_sales_by_category", ["orders", "products"])


def test_refresh_non_existent_mv_raises_error(db_manager):
    with pytest.raises(ValueError, match="does not exist"):
        db_manager.refresh_materialized_view("non_existent_mv")
