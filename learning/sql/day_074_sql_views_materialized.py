import sqlite3
import time
from typing import Any, Dict, List


class SQLViewManager:
    """Manages standard SQL views and simulated Materialized Views in SQLite."""

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_metadata_table()

    def _init_metadata_table(self) -> None:
        """Initialize system tables for tracking materialized views and table updates."""
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS _mv_metadata (
                    mv_name TEXT PRIMARY KEY,
                    select_query TEXT NOT NULL,
                    last_refreshed_at REAL NOT NULL
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS _table_modifications (
                    table_name TEXT PRIMARY KEY,
                    last_modified_at REAL NOT NULL
                )
                """
            )

    def log_table_modification(self, table_name: str) -> None:
        """Record modification timestamp for a source table."""
        now = time.time()
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO _table_modifications (table_name, last_modified_at)
                VALUES (?, ?)
                ON CONFLICT(table_name) DO UPDATE SET last_modified_at = excluded.last_modified_at
                """,
                (table_name, now),
            )

    def setup_schema(self) -> None:
        """Set up standard tables: products, customers, orders."""
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY,
                    customer_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    order_date TEXT NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES products (product_id)
                )
                """
            )
        self.log_table_modification("products")
        self.log_table_modification("orders")

    def insert_product(self, product_id: int, name: str, category: str, price: float) -> None:
        """Insert a product and log modification."""
        with self.conn:
            self.conn.execute(
                "INSERT INTO products (product_id, name, category, price) VALUES (?, ?, ?, ?)",
                (product_id, name, category, price),
            )
        self.log_table_modification("products")

    def insert_order(self, order_id: int, customer_id: int, product_id: int, quantity: int, order_date: str) -> None:
        """Insert an order and log modification."""
        with self.conn:
            self.conn.execute(
                "INSERT INTO orders (order_id, customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?, ?)",
                (order_id, customer_id, product_id, quantity, order_date),
            )
        self.log_table_modification("orders")

    def create_standard_view(self, view_name: str, select_query: str) -> None:
        """Create a standard SQL View (computed dynamically on query)."""
        with self.conn:
            self.conn.execute(f"DROP VIEW IF EXISTS {view_name}")
            self.conn.execute(f"CREATE VIEW {view_name} AS {select_query}")

    def create_materialized_view(self, mv_name: str, select_query: str) -> None:
        """Create a simulated Materialized View backed by a concrete table."""
        with self.conn:
            self.conn.execute(f"DROP TABLE IF EXISTS {mv_name}")
            self.conn.execute(f"CREATE TABLE {mv_name} AS {select_query}")
            now = time.time()
            self.conn.execute(
                """
                INSERT INTO _mv_metadata (mv_name, select_query, last_refreshed_at)
                VALUES (?, ?, ?)
                ON CONFLICT(mv_name) DO UPDATE SET select_query=excluded.select_query, last_refreshed_at=excluded.last_refreshed_at
                """,
                (mv_name, select_query, now),
            )

    def refresh_materialized_view(self, mv_name: str) -> None:
        """Refresh a Materialized View by recomputing the backing table."""
        cursor = self.conn.execute("SELECT select_query FROM _mv_metadata WHERE mv_name = ?", (mv_name,))
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Materialized view '{mv_name}' does not exist in metadata.")

        select_query = row["select_query"]
        with self.conn:
            self.conn.execute(f"DROP TABLE IF EXISTS {mv_name}")
            self.conn.execute(f"CREATE TABLE {mv_name} AS {select_query}")
            now = time.time()
            self.conn.execute(
                "UPDATE _mv_metadata SET last_refreshed_at = ? WHERE mv_name = ?",
                (now, mv_name),
            )

    def is_materialized_view_stale(self, mv_name: str, source_tables: List[str]) -> bool:
        """Check if any source table was modified after the last materialized view refresh."""
        cursor = self.conn.execute("SELECT last_refreshed_at FROM _mv_metadata WHERE mv_name = ?", (mv_name,))
        mv_row = cursor.fetchone()
        if not mv_row:
            raise ValueError(f"Materialized view '{mv_name}' not found.")

        last_refreshed = mv_row["last_refreshed_at"]
        placeholders = ",".join("?" for _ in source_tables)
        cursor = self.conn.execute(
            f"SELECT MAX(last_modified_at) as max_mod FROM _table_modifications WHERE table_name IN ({placeholders})",
            source_tables,
        )
        mod_row = cursor.fetchone()
        if mod_row and mod_row["max_mod"] is not None:
            return mod_row["max_mod"] > last_refreshed
        return False

    def fetch_all(self, query_str: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute query and return results as list of dictionaries."""
        cursor = self.conn.execute(query_str, params)
        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        self.conn.close()
