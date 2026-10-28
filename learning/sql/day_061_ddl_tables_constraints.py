"""
SQL DDL: Tables and Constraints Demonstration using SQLite.

This module demonstrates SQL Data Definition Language (DDL) concepts including:
- Table creation (CREATE TABLE)
- Primary key constraints (PRIMARY KEY)
- Foreign key constraints (FOREIGN KEY ... REFERENCES ... ON DELETE RESTRICT)
- Unique constraints (UNIQUE)
- Check constraints (CHECK)
- Default values (DEFAULT)
- Schema introspection via SQLite PRAGMA commands
"""

import sqlite3
from typing import Dict, List, Optional, Any


class DatabaseSchemaManager:
    """Manages SQLite schema creation, data insertion, and constraint enforcement."""

    def __init__(self, db_path: str = ":memory:") -> None:
        """Initialize database connection and enable foreign key support."""
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        # SQLite disables foreign key enforcement by default per connection
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def create_tables(self) -> None:
        """Create departments and employees tables with strict constraints."""
        ddl_departments = """
        CREATE TABLE IF NOT EXISTS departments (
            dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dept_name TEXT NOT NULL UNIQUE,
            budget REAL NOT NULL CHECK(budget >= 0)
        );
        """

        ddl_employees = """
        CREATE TABLE IF NOT EXISTS employees (
            emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            salary REAL NOT NULL CHECK(salary > 0),
            dept_id INTEGER NOT NULL,
            hire_date TEXT DEFAULT (DATE('now')),
            FOREIGN KEY (dept_id) REFERENCES departments (dept_id) ON DELETE RESTRICT ON UPDATE CASCADE
        );
        """

        with self.conn:
            self.conn.execute(ddl_departments)
            self.conn.execute(ddl_employees)

    def add_department(self, dept_name: str, budget: float) -> int:
        """Insert a department and return its auto-generated ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO departments (dept_name, budget) VALUES (?, ?);",
            (dept_name, budget)
        )
        self.conn.commit()
        return cursor.lastrowid

    def add_employee(
        self,
        emp_name: str,
        email: str,
        salary: float,
        dept_id: int,
        hire_date: Optional[str] = None
    ) -> int:
        """Insert an employee into the database."""
        cursor = self.conn.cursor()
        if hire_date:
            cursor.execute(
                """
                INSERT INTO employees (emp_name, email, salary, dept_id, hire_date)
                VALUES (?, ?, ?, ?, ?);
                """,
                (emp_name, email, salary, dept_id, hire_date)
            )
        else:
            cursor.execute(
                """
                INSERT INTO employees (emp_name, email, salary, dept_id)
                VALUES (?, ?, ?, ?);
                """,
                (emp_name, email, salary, dept_id)
            )
        self.conn.commit()
        return cursor.lastrowid

    def delete_department(self, dept_id: int) -> bool:
        """Delete a department by ID."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM departments WHERE dept_id = ?;", (dept_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_table_columns(self, table_name: str) -> List[Dict[str, Any]]:
        """Retrieve column information for a table using PRAGMA table_info."""
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        rows = cursor.fetchall()
        return [
            {
                "cid": row["cid"],
                "name": row["name"],
                "type": row["type"],
                "notnull": bool(row["notnull"]),
                "dflt_value": row["dflt_value"],
                "pk": bool(row["pk"])
            }
            for row in rows
        ]

    def get_foreign_keys(self, table_name: str) -> List[Dict[str, Any]]:
        """Retrieve foreign key details for a table using PRAGMA foreign_key_list."""
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        rows = cursor.fetchall()
        return [
            {
                "id": row["id"],
                "table": row["table"],
                "from": row["from"],
                "to": row["to"],
                "on_delete": row["on_delete"],
                "on_update": row["on_update"]
            }
            for row in rows
        ]

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()
