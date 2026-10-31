import pytest
from learning.sql.day_064_sql_aggregations_group_by import SalesAnalyticsDB


@pytest.fixture
def sample_sales_records():
    return [
        {"customer_id": 1, "product_category": "Electronics", "region": "North", "order_date": "2023-01-15", "status": "completed", "amount": 250.0},
        {"customer_id": 1, "product_category": "Electronics", "region": "North", "order_date": "2023-01-20", "status": "completed", "amount": 150.0},
        {"customer_id": 2, "product_category": "Books", "region": "South", "order_date": "2023-01-18", "status": "pending", "amount": 30.0},
        {"customer_id": 2, "product_category": "Electronics", "region": "South", "order_date": "2023-02-10", "status": "completed", "amount": 500.0},
        {"customer_id": 3, "product_category": "Books", "region": "North", "order_date": "2023-02-14", "status": "cancelled", "amount": 45.0},
        {"customer_id": 3, "product_category": "Clothing", "region": "North", "order_date": "2023-02-28", "status": "completed", "amount": 100.0},
    ]


@pytest.fixture
def analytics_db(sample_sales_records):
    db = SalesAnalyticsDB(":memory:")
    db.seed_data(sample_sales_records)
    yield db
    db.close()


def test_category_summary(analytics_db):
    summary = analytics_db.get_category_summary()
    assert len(summary) == 3

    electronics = next(item for item in summary if item["product_category"] == "Electronics")
    assert electronics["total_orders"] == 3
    assert electronics["total_revenue"] == 900.0
    assert electronics["avg_order_value"] == 300.0
    assert electronics["min_order_value"] == 150.0
    assert electronics["max_order_value"] == 500.0


def test_high_value_customers(analytics_db):
    high_spenders = analytics_db.get_high_value_customers(min_spend=300.0)
    assert len(high_spenders) == 2

    cust_ids = [row["customer_id"] for row in high_spenders]
    assert 1 in cust_ids
    assert 2 in cust_ids
    assert 3 not in cust_ids


def test_regional_status_breakdown(analytics_db):
    breakdown = analytics_db.get_regional_status_breakdown()
    assert len(breakdown) == 2

    north = next(item for item in breakdown if item["region"] == "North")
    assert north["total_orders"] == 4
    assert north["completed_orders"] == 3
    assert north["cancelled_orders"] == 1
    assert north["completed_revenue"] == 500.0


def test_monthly_category_sales(analytics_db):
    monthly = analytics_db.get_monthly_category_sales()
    assert len(monthly) == 5

    jan_electronics = next(
        item for item in monthly if item["sales_month"] == "2023-01" and item["product_category"] == "Electronics"
    )
    assert jan_electronics["total_orders"] == 2
    assert jan_electronics["monthly_revenue"] == 400.0


def test_empty_database():
    db = SalesAnalyticsDB(":memory:")
    summary = db.get_category_summary()
    assert summary == []
    high_spenders = db.get_high_value_customers(100.0)
    assert high_spenders == []
    db.close()
