"""
Unit tests for SQL join queries.
"""

import pytest
from learning.sql.day_065_sql_joins import SQLJoinAnalyzer


@pytest.fixture
def analyzer():
    """Fixture providing an initialized SQLJoinAnalyzer instance."""
    db = SQLJoinAnalyzer()
    yield db
    db.close()


def test_raw_tables(analyzer):
    """Test table initialization."""
    employees = analyzer.get_raw_table("employees")
    departments = analyzer.get_raw_table("departments")

    assert len(employees) == 4
    assert len(departments) == 4

    with pytest.raises(ValueError):
        analyzer.get_raw_table("invalid_table")


def test_inner_join(analyzer):
    """INNER JOIN should return only rows with matching foreign keys."""
    results = analyzer.inner_join()
    # 3 employees have valid dept_ids (Alice:10, Bob:20, Charlie:10)
    assert len(results) == 3

    names = [row["emp_name"] for row in results]
    assert "Alice" in names
    assert "Bob" in names
    assert "Charlie" in names
    assert "David" not in names  # David has NULL dept_id


def test_left_join(analyzer):
    """LEFT JOIN should return all employees, filling missing dept info with NULL."""
    results = analyzer.left_join()
    assert len(results) == 4

    david_row = next(r for r in results if r["emp_name"] == "David")
    assert david_row["dept_id"] is None
    assert david_row["dept_name"] is None


def test_right_join(analyzer):
    """RIGHT JOIN should return all departments, including ones without employees."""
    results = analyzer.right_join()
    # Departments 10 (2 emps), 20 (1 emp), 30 (0 emps), 40 (0 emps)
    # Dept 10 -> Alice, Charlie; Dept 20 -> Bob; Dept 30 -> NULL; Dept 40 -> NULL
    dept_names = [r["dept_name"] for r in results]
    assert "Engineering" in dept_names
    assert "Marketing" in dept_names
    assert "Sales" in dept_names
    assert "Research" in dept_names

    research_rows = [r for r in results if r["dept_name"] == "Research"]
    assert len(research_rows) == 1
    assert research_rows[0]["emp_id"] is None


def test_full_outer_join(analyzer):
    """FULL OUTER JOIN returns union of both tables (5 unique records)."""
    results = analyzer.full_outer_join()
    # 3 inner matches + 1 employee without dept (David) + 2 depts without emps (Sales, Research)
    # Total rows: 3 (inner) + 1 (David) + 2 (Sales, Research) = 6 rows
    assert len(results) == 6

    david = next((r for r in results if r["emp_name"] == "David"), None)
    research = next((r for r in results if r["dept_name"] == "Research"), None)
    sales = next((r for r in results if r["dept_name"] == "Sales"), None)

    assert david is not None and david["dept_name"] is None
    assert research is not None and research["emp_name"] is None
    assert sales is not None and sales["emp_name"] is None
