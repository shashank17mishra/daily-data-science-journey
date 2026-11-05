import pytest
from learning.sql.day_069_sql_ctes import CTEAnalyticsManager


@pytest.fixture
def analytics_db():
    manager = CTEAnalyticsManager(":memory:")
    manager.seed_data()
    yield manager
    manager.close()


def test_schema_and_seed_data(analytics_db):
    cursor = analytics_db.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employees")
    emp_count = cursor.fetchone()[0]
    assert emp_count == 8

    cursor.execute("SELECT COUNT(*) FROM sales")
    sales_count = cursor.fetchone()[0]
    assert sales_count == 8


def test_get_department_sales_summary(analytics_db):
    summary = analytics_db.get_department_sales_summary()
    assert len(summary) == 3

    dept_names = [row["dept_name"] for row in summary]
    assert dept_names[0] == "Sales"
    assert summary[0]["total_sales"] == 89000.0

    avg_dept_sales = (89000.0 + 5000.0 + 3000.0) / 3.0
    assert summary[0]["company_avg_dept_sales"] == round(avg_dept_sales, 2)
    assert summary[0]["is_above_average"] == 1
    assert summary[1]["is_above_average"] == 0


def test_get_employee_hierarchy_full(analytics_db):
    hierarchy = analytics_db.get_employee_hierarchy(root_emp_id=1)
    assert len(hierarchy) == 8

    root = hierarchy[0]
    assert root["emp_id"] == 1
    assert root["name"] == "Alice (CEO)"
    assert root["level"] == 0
    assert root["path"] == "Alice (CEO)"

    evan = next(emp for emp in hierarchy if emp["name"] == "Evan (Senior Eng)")
    assert evan["level"] == 3
    assert evan["path"] == "Alice (CEO) -> Bob (VP Eng) -> Diana (Lead Eng) -> Evan (Senior Eng)"


def test_get_employee_hierarchy_sub_tree(analytics_db):
    hierarchy = analytics_db.get_employee_hierarchy(root_emp_id=2)
    assert len(hierarchy) == 3

    names = [row["name"] for row in hierarchy]
    assert "Bob (VP Eng)" in names
    assert "Diana (Lead Eng)" in names
    assert "Evan (Senior Eng)" in names
    assert "Alice (CEO)" not in names


def test_get_top_performers_by_department(analytics_db):
    top1 = analytics_db.get_top_performers_by_department(rank_limit=1)
    dept_ranks = {row["dept_name"]: row["sales_rank"] for row in top1}
    assert all(rank == 1 for rank in dept_ranks.values())

    sales_top1 = next(row for row in top1 if row["dept_name"] == "Sales")
    assert sales_top1["employee_name"] == "Charlie (VP Sales)"
    assert sales_top1["total_sales"] == 37000.0

    top2 = analytics_db.get_top_performers_by_department(rank_limit=2)
    sales_top2_names = [row["employee_name"] for row in top2 if row["dept_name"] == "Sales"]
    assert len(sales_top2_names) == 2
    assert "Charlie (VP Sales)" in sales_top2_names
    assert "George (Sales Rep)" in sales_top2_names
