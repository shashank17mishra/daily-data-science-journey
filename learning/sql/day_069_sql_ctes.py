import sqlite3
from typing import Any, Dict, List


class CTEAnalyticsManager:
    """Demonstrates SQL Common Table Expressions (CTEs) using SQLite.

    Includes non-recursive CTEs for multi-stage aggregation, recursive CTEs
    for hierarchical tree traversals, and window functions within CTEs.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self) -> None:
        """Create sample tables: departments, employees, and sales."""
        cursor = self.conn.cursor()
        cursor.executescript("""
            CREATE TABLE departments (
                dept_id INTEGER PRIMARY KEY,
                dept_name TEXT NOT NULL
            );

            CREATE TABLE employees (
                emp_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                manager_id INTEGER,
                dept_id INTEGER,
                salary REAL NOT NULL,
                FOREIGN KEY (manager_id) REFERENCES employees(emp_id),
                FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
            );

            CREATE TABLE sales (
                sale_id INTEGER PRIMARY KEY,
                emp_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                sale_date TEXT NOT NULL,
                FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
            );
        """)
        self.conn.commit()

    def seed_data(self) -> None:
        """Seed tables with mock organizational and sales data."""
        cursor = self.conn.cursor()

        departments = [
            (1, "Engineering"),
            (2, "Sales"),
            (3, "Marketing"),
        ]
        cursor.executemany("INSERT INTO departments VALUES (?, ?)", departments)

        employees = [
            (1, "Alice (CEO)", None, 1, 150000.0),
            (2, "Bob (VP Eng)", 1, 1, 120000.0),
            (3, "Charlie (VP Sales)", 1, 2, 115000.0),
            (4, "Diana (Lead Eng)", 2, 1, 95000.0),
            (5, "Evan (Senior Eng)", 4, 1, 85000.0),
            (6, "Fiona (Sales Mgr)", 3, 2, 90000.0),
            (7, "George (Sales Rep)", 6, 2, 65000.0),
            (8, "Hannah (Mktg Mgr)", 1, 3, 88000.0),
        ]
        cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees)

        sales = [
            (1, 3, 15000.0, "2023-01-10"),
            (2, 3, 22000.0, "2023-01-15"),
            (3, 6, 8000.0, "2023-01-20"),
            (4, 7, 12000.0, "2023-01-22"),
            (5, 7, 18000.0, "2023-02-01"),
            (6, 4, 5000.0, "2023-02-05"),
            (7, 6, 14000.0, "2023-02-10"),
            (8, 8, 3000.0, "2023-02-12"),
        ]
        cursor.executemany("INSERT INTO sales VALUES (?, ?, ?, ?)", sales)
        self.conn.commit()

    def get_department_sales_summary(self) -> List[Dict[str, Any]]:
        """Calculate department sales summaries and compare with company average.

        Uses chained CTEs (dept_sales -> company_avg).
        """
        query = """
        WITH dept_sales AS (
            SELECT
                e.dept_id,
                d.dept_name,
                SUM(s.amount) AS total_sales,
                COUNT(s.sale_id) AS sale_count
            FROM sales s
            JOIN employees e ON s.emp_id = e.emp_id
            JOIN departments d ON e.dept_id = d.dept_id
            GROUP BY e.dept_id, d.dept_name
        ),
        company_avg AS (
            SELECT AVG(total_sales) AS avg_dept_sales
            FROM dept_sales
        )
        SELECT
            ds.dept_id,
            ds.dept_name,
            ds.total_sales,
            ds.sale_count,
            ROUND(ca.avg_dept_sales, 2) AS company_avg_dept_sales,
            CASE
                WHEN ds.total_sales >= ca.avg_dept_sales THEN 1
                ELSE 0
            END AS is_above_average
        FROM dept_sales ds
        CROSS JOIN company_avg ca
        ORDER BY ds.total_sales DESC;
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def get_employee_hierarchy(self, root_emp_id: int = 1) -> List[Dict[str, Any]]:
        """Retrieve organizational hierarchy starting from a given manager using a RECURSIVE CTE."""
        query = """
        WITH RECURSIVE org_chart AS (
            SELECT
                emp_id,
                name,
                manager_id,
                dept_id,
                0 AS level,
                name AS path
            FROM employees
            WHERE emp_id = ?

            UNION ALL

            SELECT
                e.emp_id,
                e.name,
                e.manager_id,
                e.dept_id,
                o.level + 1,
                o.path || ' -> ' || e.name
            FROM employees e
            JOIN org_chart o ON e.manager_id = o.emp_id
        )
        SELECT
            emp_id,
            name,
            manager_id,
            level,
            path
        FROM org_chart
        ORDER BY level, emp_id;
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (root_emp_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_top_performers_by_department(self, rank_limit: int = 1) -> List[Dict[str, Any]]:
        """Rank sales representatives within each department using window functions inside a CTE."""
        query = """
        WITH emp_sales AS (
            SELECT
                e.emp_id,
                e.name AS employee_name,
                d.dept_name,
                COALESCE(SUM(s.amount), 0.0) AS total_sales
            FROM employees e
            JOIN departments d ON e.dept_id = d.dept_id
            LEFT JOIN sales s ON e.emp_id = s.emp_id
            GROUP BY e.emp_id, e.name, d.dept_name
        ),
        ranked_emp AS (
            SELECT
                emp_id,
                employee_name,
                dept_name,
                total_sales,
                DENSE_RANK() OVER (PARTITION BY dept_name ORDER BY total_sales DESC) AS sales_rank
            FROM emp_sales
        )
        SELECT
            emp_id,
            employee_name,
            dept_name,
            total_sales,
            sales_rank
        FROM ranked_emp
        WHERE sales_rank <= ?
        ORDER BY dept_name, sales_rank;
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (rank_limit,))
        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        """Close connection."""
        self.conn.close()
