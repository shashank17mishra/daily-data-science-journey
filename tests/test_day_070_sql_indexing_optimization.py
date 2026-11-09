import sqlite3
import pytest
from learning.sql.day_070_sql_indexing_optimization import QueryOptimizer


@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()


@pytest.fixture
def optimizer(db_conn):
    opt = QueryOptimizer(db_conn)
    opt.create_schema_and_data(num_records=1000)
    return opt


def test_schema_and_data_population(optimizer, db_conn):
    cursor = db_conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders")
    count = cursor.fetchone()[0]
    assert count == 1000


def test_unindexed_query_plan(optimizer):
    query = "SELECT * FROM orders WHERE customer_id = ? AND status = ?"
    params = (25, "COMPLETED")

    plan = optimizer.get_query_plan(query, params)
    assert len(plan) > 0
    assert not optimizer.uses_index(query, params)
    assert any("SCAN TABLE" in line or "SCAN orders" in line for line in plan)


def test_single_index_optimization(optimizer):
    query = "SELECT * FROM orders WHERE customer_id = ?"
    params = (25,)

    assert not optimizer.uses_index(query, params)

    optimizer.create_single_index("idx_orders_customer", "orders", "customer_id")

    assert optimizer.uses_index(query, params)
    plan = optimizer.get_query_plan(query, params)
    assert any("USING INDEX" in line for line in plan)


def test_composite_index_optimization(optimizer):
    query = "SELECT id, status, total_amount FROM orders WHERE status = ? AND customer_id = ?"
    params = ("COMPLETED", 15)

    res_before = optimizer.execute_and_measure(query, params, iterations=3)
    assert not res_before["uses_index"]

    optimizer.create_composite_index("idx_orders_status_customer", "orders", ["status", "customer_id"])

    res_after = optimizer.execute_and_measure(query, params, iterations=3)
    assert res_after["uses_index"]
    assert res_before["result_count"] == res_after["result_count"]
    assert res_before["results"] == res_after["results"]


def test_query_plan_analysis(optimizer):
    query = "SELECT * FROM orders WHERE total_amount > 200.0"
    plan = optimizer.get_query_plan(query)
    assert isinstance(plan, list)
    assert len(plan) > 0
