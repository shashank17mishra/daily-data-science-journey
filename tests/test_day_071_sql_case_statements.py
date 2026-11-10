import pytest
from learning.sql.day_071_sql_case_statements import SQLCaseAnalyzer


@pytest.fixture
def sql_analyzer():
    analyzer = SQLCaseAnalyzer(":memory:")
    yield analyzer
    analyzer.close()


def test_customer_tiers(sql_analyzer):
    tiers = sql_analyzer.get_customer_tiers()
    assert len(tiers) == 5

    tier_map = {row["name"]: row["tier"] for row in tiers}
    spend_map = {row["name"]: row["total_spent"] for row in tiers}

    assert tier_map["Diana Prince"] == "VIP"
    assert spend_map["Diana Prince"] == 1500.0

    assert tier_map["Alice Smith"] == "VIP"
    assert spend_map["Alice Smith"] == 1100.0

    assert tier_map["Bob Jones"] == "Silver"
    assert spend_map["Bob Jones"] == 350.0

    assert tier_map["Charlie Brown"] == "Bronze"
    assert spend_map["Charlie Brown"] == 50.0

    assert tier_map["Evan Wright"] == "Bronze"
    assert spend_map["Evan Wright"] == 0.0


def test_inventory_status(sql_analyzer):
    inventory = sql_analyzer.get_inventory_status()
    assert len(inventory) == 4

    status_map = {row["product_name"]: row["stock_status"] for row in inventory}
    contact_map = {row["product_name"]: row["contact_info"] for row in inventory}

    assert status_map["Laptop"] == "OUT_OF_STOCK"
    assert contact_map["Laptop"] == "supplier_a@example.com"

    assert status_map["Mouse"] == "REORDER_NOW"
    assert contact_map["Mouse"] == "NO_CONTACT_INFO"

    assert status_map["Keyboard"] == "LOW_STOCK"

    assert status_map["Monitor"] == "SUFFICIENT"


def test_regional_order_summary(sql_analyzer):
    summary = sql_analyzer.get_regional_order_summary()
    assert len(summary) == 4

    summary_map = {row["region"]: row for row in summary}

    north = summary_map["North"]
    assert north["total_orders"] == 2
    assert north["completed_orders"] == 2
    assert north["pending_orders"] == 0
    assert north["cancelled_orders"] == 0
    assert north["completion_rate"] == 100.0

    south = summary_map["South"]
    assert south["total_orders"] == 2
    assert south["completed_orders"] == 1
    assert south["pending_orders"] == 1
    assert south["completion_rate"] == 50.0

    west = summary_map["West"]
    assert west["completion_rate"] == 50.0

    east = summary_map["East"]
    assert east["total_orders"] == 1
    assert east["completed_orders"] == 0
    assert east["cancelled_orders"] == 1
    assert east["completion_rate"] == 0.0
