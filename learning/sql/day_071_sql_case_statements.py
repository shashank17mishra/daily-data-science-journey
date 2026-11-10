import sqlite3
from typing import Dict, List, Any


class SQLCaseAnalyzer:
    """Demonstrates intermediate SQL techniques using CASE statements,
    COALESCE, NULLIF, and conditional aggregation in SQLite.
    """

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._setup_schema_and_data()

    def _setup_schema_and_data(self) -> None:
        """Creates tables and populates seed data for analysis."""
        cursor = self.conn.cursor()

        cursor.executescript("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            region TEXT NOT NULL
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            region TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        );

        CREATE TABLE inventory (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            stock_quantity INTEGER NOT NULL,
            reorder_level INTEGER NOT NULL,
            supplier_contact TEXT
        );

        INSERT INTO customers (customer_id, name, region) VALUES
            (1, 'Alice Smith', 'North'),
            (2, 'Bob Jones', 'South'),
            (3, 'Charlie Brown', 'East'),
            (4, 'Diana Prince', 'West'),
            (5, 'Evan Wright', 'North');

        INSERT INTO orders (order_id, customer_id, amount, status, region) VALUES
            (101, 1, 600.0, 'completed', 'North'),
            (102, 1, 500.0, 'completed', 'North'),
            (103, 2, 200.0, 'completed', 'South'),
            (104, 2, 150.0, 'pending', 'South'),
            (105, 3, 50.0, 'cancelled', 'East'),
            (106, 4, 1200.0, 'completed', 'West'),
            (107, 4, 300.0, 'pending', 'West');

        INSERT INTO inventory (product_id, product_name, stock_quantity, reorder_level, supplier_contact) VALUES
            (1, 'Laptop', 0, 10, 'supplier_a@example.com'),
            (2, 'Mouse', 5, 10, NULL),
            (3, 'Keyboard', 12, 10, 'supplier_b@example.com'),
            (4, 'Monitor', 50, 15, NULL);
        """)
        self.conn.commit()

    def get_customer_tiers(self) -> List[Dict[str, Any]]:
        """Categorizes customers into spend tiers using SQL CASE statements.

        Tiers:
        - Spend >= 1000 -> 'VIP'
        - Spend >= 500  -> 'Gold'
        - Spend >= 100  -> 'Silver'
        - Spend < 100   -> 'Bronze'
        """
        query = """
        SELECT
            c.customer_id,
            c.name,
            COALESCE(SUM(o.amount), 0.0) AS total_spent,
            CASE
                WHEN COALESCE(SUM(o.amount), 0.0) >= 1000.0 THEN 'VIP'
                WHEN COALESCE(SUM(o.amount), 0.0) >= 500.0 THEN 'Gold'
                WHEN COALESCE(SUM(o.amount), 0.0) >= 100.0 THEN 'Silver'
                ELSE 'Bronze'
            END AS tier
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
        ORDER BY total_spent DESC, c.customer_id ASC;
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def get_inventory_status(self) -> List[Dict[str, Any]]:
        """Evaluates inventory levels and cleans contact info using CASE and COALESCE."""
        query = """
        SELECT
            product_id,
            product_name,
            stock_quantity,
            reorder_level,
            CASE
                WHEN stock_quantity = 0 THEN 'OUT_OF_STOCK'
                WHEN stock_quantity <= reorder_level THEN 'REORDER_NOW'
                WHEN stock_quantity <= reorder_level * 1.5 THEN 'LOW_STOCK'
                ELSE 'SUFFICIENT'
            END AS stock_status,
            COALESCE(supplier_contact, 'NO_CONTACT_INFO') AS contact_info
        FROM inventory
        ORDER BY product_id ASC;
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def get_regional_order_summary(self) -> List[Dict[str, Any]]:
        """Computes regional order statistics using conditional aggregation (SUM with CASE)."""
        query = """
        SELECT
            region,
            COUNT(order_id) AS total_orders,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_orders,
            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending_orders,
            SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
            ROUND(
                100.0 * SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) /
                NULLIF(COUNT(order_id), 0),
                2
            ) AS completion_rate
        FROM orders
        GROUP BY region
        ORDER BY region ASC;
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        """Closes the underlying database connection."""
        self.conn.close()
