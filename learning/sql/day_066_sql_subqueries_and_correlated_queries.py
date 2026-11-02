import sqlite3
from typing import Any, Dict, List


def create_and_seed_db(conn: sqlite3.Connection) -> None:
    """Creates tables and populates sample data for database queries."""
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE departments (
            department_id INTEGER PRIMARY KEY,
            department_name TEXT NOT NULL,
            location TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE employees (
            employee_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            department_id INTEGER,
            salary REAL NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments(department_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE project_assignments (
            assignment_id INTEGER PRIMARY KEY,
            employee_id INTEGER NOT NULL,
            project_name TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        );
    """)

    departments = [
        (1, "Engineering", "New York"),
        (2, "Sales", "Chicago"),
        (3, "Marketing", "New York"),
        (4, "HR", "San Francisco"),
    ]
    cursor.executemany(
        "INSERT INTO departments VALUES (?, ?, ?);", departments
    )

    employees = [
        (101, "Alice", "Smith", 1, 95000.0),
        (102, "Bob", "Jones", 1, 80000.0),
        (103, "Charlie", "Brown", 1, 110000.0),
        (104, "Diana", "Prince", 2, 60000.0),
        (105, "Evan", "Wright", 2, 75000.0),
        (106, "Fiona", "Gallagher", 3, 70000.0),
        (107, "George", "Clark", 3, 65000.0),
        (108, "Hannah", "Abbott", 4, 50000.0),
    ]
    cursor.executemany(
        "INSERT INTO employees VALUES (?, ?, ?, ?, ?);", employees
    )

    assignments = [
        (1, 101, "Alpha"),
        (2, 101, "Beta"),
        (3, 102, "Alpha"),
        (4, 103, "Gamma"),
        (5, 104, "Delta"),
        (6, 105, "Epsilon"),
    ]
    cursor.executemany(
        "INSERT INTO project_assignments VALUES (?, ?, ?);", assignments
    )

    conn.commit()


def get_employees_above_company_avg(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Return employees earning strictly above the overall company average salary.

    Uses a non-correlated (scalar) subquery in the WHERE clause.
    """
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
        SELECT employee_id, first_name, last_name, salary
        FROM employees
        WHERE salary > (
            SELECT AVG(salary)
            FROM employees
        )
        ORDER BY salary DESC;
    """
    cursor.execute(query)
    return [dict(row) for row in cursor.fetchall()]


def get_employees_above_dept_avg(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Return employees who earn strictly more than the average salary of their own department.

    Uses a correlated subquery in the WHERE clause referencing the outer table alias (e1).
    """
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
        SELECT e1.employee_id, e1.first_name, e1.last_name, e1.department_id, e1.salary
        FROM employees e1
        WHERE e1.salary > (
            SELECT AVG(e2.salary)
            FROM employees e2
            WHERE e2.department_id = e1.department_id
        )
        ORDER BY e1.department_id, e1.salary DESC;
    """
    cursor.execute(query)
    return [dict(row) for row in cursor.fetchall()]


def get_employee_salary_diffs(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Return employee details alongside their salary difference from their department average.

    Uses a correlated subquery in the SELECT clause.
    """
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
        SELECT
            e1.employee_id,
            e1.first_name,
            e1.last_name,
            e1.salary,
            ROUND(e1.salary - (
                SELECT AVG(e2.salary)
                FROM employees e2
                WHERE e2.department_id = e1.department_id
            ), 2) AS diff_from_dept_avg
        FROM employees e1
        ORDER BY e1.employee_id;
    """
    cursor.execute(query)
    return [dict(row) for row in cursor.fetchall()]


def get_departments_with_high_earners(
    conn: sqlite3.Connection, min_salary: float
) -> List[Dict[str, Any]]:
    """Return departments that have at least one employee with salary >= min_salary.

    Uses a correlated subquery with EXISTS.
    """
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
        SELECT d.department_id, d.department_name, d.location
        FROM departments d
        WHERE EXISTS (
            SELECT 1
            FROM employees e
            WHERE e.department_id = d.department_id
              AND e.salary >= ?
        )
        ORDER BY d.department_id;
    """
    cursor.execute(query, (min_salary,))
    return [dict(row) for row in cursor.fetchall()]


def get_employees_without_projects(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Return employees who are NOT assigned to any project.

    Uses a correlated subquery with NOT EXISTS.
    """
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = """
        SELECT e.employee_id, e.first_name, e.last_name
        FROM employees e
        WHERE NOT EXISTS (
            SELECT 1
            FROM project_assignments pa
            WHERE pa.employee_id = e.employee_id
        )
        ORDER BY e.employee_id;
    """
    cursor.execute(query)
    return [dict(row) for row in cursor.fetchall()]
