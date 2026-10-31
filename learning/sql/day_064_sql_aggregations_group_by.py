"""
SQL Aggregations & Group By Demonstration using SQLite.
Includes aggregation functions (COUNT, SUM, AVG, MIN, MAX),
GROUP BY, HAVING, and conditional aggregation with CASE WHEN.
"""

import sqlite3
from typing import Any, Dict, List


class SalesAnalyticsDB:
    """Manages an in-memory SQLite database for sales analytics queries."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._setup_schema()

    def _setup_schema(self) -> None:
        """Create sales table if it does not exist."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product_category TEXT NOT NULL,
                region TEXT NOT NULL,
                order_date TEXT NOT NULL,
                status TEXT NOT NULL,
                amount REAL NOT NULL
            )
        """)
        self.conn.commit()

    def seed_data(self, records: List[Dict[str, Any]]) -> None:
        """Seed database with sales records."""
        cursor = self.conn.cursor()
        cursor.executemany("""
            INSERT INTO sales (customer_id, product_category, region, order_date, status, amount)
            VALUES (:customer_id, :product_category, :region, :order_date, :status, :amount)
        """, records)
        self.conn.commit()

    def get_category_summary(self) -> List[Dict[str, Any]]:
        """
        Aggregate sales statistics by product category.
        Uses SUM, AVG, COUNT, MIN, MAX with GROUP BY.
        """
        query = """
            SELECT
                product_category,
                COUNT(*) AS total_orders,
                ROUND(SUM(amount), 2) AS total_revenue,
                ROUND(AVG(amount), 2) AS avg_order_value,
                ROUND(MIN(amount), 2) AS min_order_value,
                ROUND(MAX(amount), 2) AS max_order_value
            FROM sales
            GROUP BY product_category
            ORDER BY total_revenue DESC
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def get_high_value_customers(self, min_spend: float) -> List[Dict[str, Any]]:
        """
        Filter aggregated results using HAVING clause.
        Returns customer_ids and total spend for customers exceeding min_spend.
        """
        query = """
            SELECT
                customer_id,
                COUNT(*) AS order_count,
                ROUND(SUM(amount), 2) AS total_spend
            FROM sales
            GROUP BY customer_id
            HAVING SUM(amount) >= ?
            ORDER BY total_spend DESC
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (min_spend,))
        return [dict(row) for row in cursor.fetchall()]

    def get_regional_status_breakdown(self) -> List[Dict[str, Any]]:
        """
        Conditional aggregation using CASE WHEN inside SUM to pivot order status counts.
        """
        query = """
            SELECT
                region,
                COUNT(*) AS total_orders,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_orders,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending_orders,
                SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
                ROUND(SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END), 2) AS completed_revenue
            FROM sales
            GROUP BY region
            ORDER BY region ASC
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def get_monthly_category_sales(self) -> List[Dict[str, Any]]:
        """
        Multi-column GROUP BY (sales_month, product_category).
        """
        query = """
            SELECT
                strftime('%Y-%m', order_date) AS sales_month,
                product_category,
                COUNT(*) AS total_orders,
                ROUND(SUM(amount), 2) AS monthly_revenue
            FROM sales
            GROUP BY strftime('%Y-%m', order_date), product_category
            ORDER BY sales_month ASC, monthly_revenue DESC
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        """Close database connection."""
        self.conn.close()
