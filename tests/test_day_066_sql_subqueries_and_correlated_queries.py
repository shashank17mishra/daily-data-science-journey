import sqlite3
import pytest
from learning.sql.day_066_sql_subqueries_and_correlated_queries import (
    create_and_seed_db,
    get_employees_above_company_avg,
    get_employees_above_dept_avg,
    get_employee_salary_diffs,
    get_departments_with_high_earners,
    get_employees_without_projects,
)


@pytest.fixture
def db_connection():
    conn = sqlite3.connect(":memory:")
    create_and_seed_db(conn)
    yield conn
    conn.close()


def test_get_employees_above_company_avg(db_connection):
    results = get_employees_above_company_avg(db_connection)
    assert len(results) == 3
    emp_ids = [r["employee_id"] for r in results]
    assert emp_ids == [103, 101, 102]


def test_get_employees_above_dept_avg(db_connection):
    results = get_employees_above_dept_avg(db_connection)
    assert len(results) == 3
    emp_ids = [r["employee_id"] for r in results]
    assert emp_ids == [103, 105, 106]


def test_get_employee_salary_diffs(db_connection):
    results = get_employee_salary_diffs(db_connection)
    assert len(results) == 8

    charlie = next(r for r in results if r["employee_id"] == 103)
    assert charlie["diff_from_dept_avg"] == 15000.0

    bob = next(r for r in results if r["employee_id"] == 102)
    assert bob["diff_from_dept_avg"] == -15000.0


def test_get_departments_with_high_earners(db_connection):
    results = get_departments_with_high_earners(db_connection, 100000.0)
    assert len(results) == 1
    assert results[0]["department_name"] == "Engineering"

    results_70k = get_departments_with_high_earners(db_connection, 70000.0)
    dept_names = [r["department_name"] for r in results_70k]
    assert "Engineering" in dept_names
    assert "Sales" in dept_names
    assert "Marketing" in dept_names
    assert "HR" not in dept_names


def test_get_employees_without_projects(db_connection):
    results = get_employees_without_projects(db_connection)
    emp_ids = [r["employee_id"] for r in results]
    assert emp_ids == [106, 107, 108]
