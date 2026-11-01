"""
Day 065: SQL Inner, Left, Right & Full Outer Joins

This module demonstrates core SQL join semantics using an in-memory SQLite database.
It handles standard ANSI SQL join queries (INNER, LEFT) and provides robust fallback
emulations (UNION-based) for database engines where RIGHT and FULL OUTER JOIN syntax
may not be natively enabled.
"""

import sqlite3
from typing import Any, Dict, List


class SQLJoinAnalyzer:
    """Manages an in-memory database to execute and demonstrate SQL join types."""

    def __init__(self) -> None:
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        """Create schema and insert deterministic test records."""
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE departments (
                dept_id INTEGER PRIMARY KEY,
                dept_name TEXT NOT NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE employees (
                emp_id INTEGER PRIMARY KEY,
                emp_name TEXT NOT NULL,
                dept_id INTEGER,
                salary REAL,
                FOREIGN KEY (dept_id) REFERENCES departments (dept_id)
            );
            """
        )

        # Departments: Dept 40 (Research) has no employees assigned
        cursor.executemany(
            "INSERT INTO departments (dept_id, dept_name) VALUES (?, ?);",
            [
                (10, "Engineering"),
                (20, "Marketing"),
                (30, "Sales"),
                (40, "Research"),
            ],
        )

        # Employees: Emp 4 (David) has NULL dept_id
        cursor.executemany(
            "INSERT INTO employees (emp_id, emp_name, dept_id, salary) VALUES (?, ?, ?, ?);",
            [
                (1, "Alice", 10, 95000.0),
                (2, "Bob", 20, 75000.0),
                (3, "Charlie", 10, 90000.0),
                (4, "David", None, 60000.0),
            ],
        )
        self.conn.commit()

    def get_raw_table(self, table_name: str) -> List[Dict[str, Any]]:
        """Fetch raw table rows as dictionaries."""
        if table_name not in {"employees", "departments"}:
            raise ValueError(f"Invalid table name: {table_name}")
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")
        return [dict(row) for row in cursor.fetchall()]

    def inner_join(self) -> List[Dict[str, Any]]:
        """
        INNER JOIN returns records with matching keys in both tables.
        Omits David (no dept) and Research (no employees).
        """
        query = """
            SELECT e.emp_id, e.emp_name, d.dept_id, d.dept_name, e.salary
            FROM employees e
            INNER JOIN departments d ON e.dept_id = d.dept_id
            ORDER BY e.emp_id;
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def left_join(self) -> List[Dict[str, Any]]:
        """
        LEFT JOIN returns all rows from left table (employees),
        and matching records from right table (departments).
        Unmatched right attributes return NULL.
        """
        query = """
            SELECT e.emp_id, e.emp_name, d.dept_id, d.dept_name, e.salary
            FROM employees e
            LEFT JOIN departments d ON e.dept_id = d.dept_id
            ORDER BY e.emp_id;
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def right_join(self) -> List[Dict[str, Any]]:
        """
        RIGHT JOIN returns all rows from right table (departments),
        and matching records from left table (employees).
        Emulated if native RIGHT JOIN is unavailable in SQLite build.
        """
        try:
            query = """
                SELECT e.emp_id, e.emp_name, d.dept_id, d.dept_name, e.salary
                FROM employees e
                RIGHT JOIN departments d ON e.dept_id = d.dept_id
                ORDER BY d.dept_id, e.emp_id;
            """
            cursor = self.conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError:
            # Swap table position using LEFT JOIN
            emulated_query = """
                SELECT e.emp_id, e.emp_name, d.dept_id, d.dept_name, e.salary
                FROM departments d
                LEFT JOIN employees e ON d.dept_id = e.dept_id
                ORDER BY d.dept_id, e.emp_id;
            """
            cursor = self.conn.cursor()
            cursor.execute(emulated_query)
            return [dict(row) for row in cursor.fetchall()]

    def full_outer_join(self) -> List[Dict[str, Any]]:
        """
        FULL OUTER JOIN returns all records from both tables.
        Unmatched columns on either side are NULL.
        Emulated using LEFT JOIN UNION ALL (RIGHT JOIN equivalent) if needed.
        """
        try:
            query = """
                SELECT e.emp_id, e.emp_name, d.dept_id, d.dept_name, e.salary
                FROM employees e
                FULL OUTER JOIN departments d ON e.dept_id = d.dept_id
                ORDER BY e.emp_id, d.dept_id;
            """
            cursor = self.conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError:
            # Emulate FULL OUTER JOIN via LEFT JOIN + UNION ALL unmatched right rows
            emulated_query = """
                SELECT e.emp_id, e.emp_name, d.dept_id, d.dept_name, e.salary
                FROM employees e
                LEFT JOIN departments d ON e.dept_id = d.dept_id
                UNION ALL
                SELECT e.emp_id, e.emp_name, d.dept_id, d.dept_name, e.salary
                FROM departments d
                LEFT JOIN employees e ON d.dept_id = e.dept_id
                WHERE e.emp_id IS NULL;
            """
            cursor = self.conn.cursor()
            cursor.execute(emulated_query)
            rows = [dict(r) for r in cursor.fetchall()]
            # Sort results for deterministic order
            return sorted(rows, key=lambda r: (r["emp_id"] if r["emp_id"] is not None else 9999, r["dept_id"] if r["dept_id"] is not None else 9999))

    def close(self) -> None:
        """Close the SQLite database connection."""
        self.conn.close()
