import sqlite3
from typing import List, Dict, Any, Optional, Tuple


class InventoryRepository:
    """Manages SQLite product inventory table using SQL DML statements."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the database schema."""
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    category TEXT NOT NULL,
                    price REAL NOT NULL CHECK(price >= 0),
                    stock INTEGER NOT NULL CHECK(stock >= 0)
                );
                """
            )

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()

    def insert_product(self, name: str, category: str, price: float, stock: int) -> int:
        """Insert a single product into the database using INSERT INTO.

        Returns:
            int: The primary key ID of the inserted record.
        """
        query = """
            INSERT INTO products (name, category, price, stock)
            VALUES (?, ?, ?, ?);
        """
        with self._conn:
            cursor = self._conn.execute(query, (name, category, price, stock))
            return cursor.lastrowid

    def bulk_insert_products(self, products: List[Tuple[str, str, float, int]]) -> int:
        """Insert multiple products in a single batch operation.

        Args:
            products: List of tuples (name, category, price, stock)

        Returns:
            int: Total number of inserted rows.
        """
        query = """
            INSERT INTO products (name, category, price, stock)
            VALUES (?, ?, ?, ?);
        """
        with self._conn:
            cursor = self._conn.executemany(query, products)
            return cursor.rowcount

    def update_product_price(self, product_id: int, new_price: float) -> bool:
        """Update the price of a specific product using UPDATE.

        Returns:
            bool: True if a record was updated, False otherwise.
        """
        query = "UPDATE products SET price = ? WHERE id = ?;"
        with self._conn:
            cursor = self._conn.execute(query, (new_price, product_id))
            return cursor.rowcount > 0

    def bulk_update_category_prices(self, category: str, percentage_change: float) -> int:
        """Adjust prices for all products in a given category by a percentage.

        Args:
            category: Product category to update.
            percentage_change: Percentage adjustment (e.g. 10.0 for +10%, -5.0 for -5%).

        Returns:
            int: Number of rows updated.
        """
        multiplier = 1.0 + (percentage_change / 100.0)
        query = """
            UPDATE products
            SET price = ROUND(price * ?, 2)
            WHERE category = ?;
        """
        with self._conn:
            cursor = self._conn.execute(query, (multiplier, category))
            return cursor.rowcount

    def update_stock(self, product_id: int, quantity_delta: int) -> bool:
        """Safely increase or decrease product stock level.

        Fails if target stock level would be negative.

        Returns:
            bool: True if update succeeded, False if product missing or stock negative.
        """
        query = """
            UPDATE products
            SET stock = stock + ?
            WHERE id = ? AND (stock + ?) >= 0;
        """
        with self._conn:
            cursor = self._conn.execute(query, (quantity_delta, product_id, quantity_delta))
            return cursor.rowcount > 0

    def delete_product(self, product_id: int) -> bool:
        """Delete a product by ID using DELETE FROM.

        Returns:
            bool: True if record was deleted, False otherwise.
        """
        query = "DELETE FROM products WHERE id = ?;"
        with self._conn:
            cursor = self._conn.execute(query, (product_id,))
            return cursor.rowcount > 0

    def delete_out_of_stock(self) -> int:
        """Delete all products where stock is zero.

        Returns:
            int: Number of deleted records.
        """
        query = "DELETE FROM products WHERE stock = 0;"
        with self._conn:
            cursor = self._conn.execute(query)
            return cursor.rowcount

    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a product by ID."""
        query = "SELECT id, name, category, price, stock FROM products WHERE id = ?;"
        cursor = self._conn.execute(query, (product_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_products(self) -> List[Dict[str, Any]]:
        """Retrieve all products."""
        query = "SELECT id, name, category, price, stock FROM products ORDER BY id;"
        cursor = self._conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]
