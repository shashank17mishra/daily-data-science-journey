"""SQL Window Functions: ROW_NUMBER and RANK implementation using SQLite.

This module demonstrates how window functions partition data, assign sequential row
numbers, calculate ranks with gaps for ties, and calculate dense ranks without gaps.
"""

import sqlite3
from typing import Any, Dict, List, Optional, Tuple


class SalesRankingAnalyzer:
    """Analyzer executing SQL window functions on employee sales data."""

    def __init__(self, db_path: str = ":memory:") -> None:
        """Initialize SQLite database connection."""
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        """Create the sales_records schema."""
        query = """
        CREATE TABLE IF NOT EXISTS sales_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            department TEXT NOT NULL,
            sales_amount REAL NOT NULL
        );
        """
        with self.conn:
            self.conn.execute(query)

    def seed_data(self, records: Optional[List[Tuple[str, str, float]]] = None) -> None:
        """Seed sample sales data into the database."""
        if records is None:
            records = [
                ("Alice", "Tech", 150000.0),
                ("Bob", "Tech", 120000.0),
                ("Charlie", "Tech", 120000.0),
                ("Diana", "Tech", 90000.0),
                ("Eve", "Sales", 200000.0),
                ("Frank", "Sales", 200000.0),
                ("Grace", "Sales", 180000.0),
                ("Heidi", "Sales", 150000.0),
            ]

        query = """
        INSERT INTO sales_records (employee_name, department, sales_amount)
        VALUES (?, ?, ?);
        """
        with self.conn:
            self.conn.executemany(query, records)

    def get_rankings(self) -> List[Dict[str, Any]]:
        """Compute ROW_NUMBER, RANK, and DENSE_RANK grouped by department.

        Returns:
            List of dictionaries containing ranking attributes for each record.
        """
        query = """
        SELECT
            employee_name,
            department,
            sales_amount,
            ROW_NUMBER() OVER (
                PARTITION BY department
                ORDER BY sales_amount DESC, employee_name ASC
            ) as row_num,
            RANK() OVER (
                PARTITION BY department
                ORDER BY sales_amount DESC
            ) as rank_val,
            DENSE_RANK() OVER (
                PARTITION BY department
                ORDER BY sales_amount DESC
            ) as dense_rank_val
        FROM sales_records
        ORDER BY department ASC, sales_amount DESC, employee_name ASC;
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def get_top_n_per_department(self, top_n: int = 1) -> List[Dict[str, Any]]:
        """Retrieve top N performers per department using RANK window function.

        Args:
            top_n: Rank threshold to include.

        Returns:
            List of dictionaries for employees with rank <= top_n.
        """
        query = """
        WITH ranked_sales AS (
            SELECT
                employee_name,
                department,
                sales_amount,
                RANK() OVER (
                    PARTITION BY department
                    ORDER BY sales_amount DESC
                ) as rank_val
            FROM sales_records
        )
        SELECT employee_name, department, sales_amount, rank_val
        FROM ranked_sales
        WHERE rank_val <= ?
        ORDER BY department ASC, rank_val ASC, employee_name ASC;
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (top_n,))
        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        """Close database connection."""
        self.conn.close()
