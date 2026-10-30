"""
SQL Filtering, Sorting, and Limiting with SQLite in Python.

This module provides a ProductRepository class that demonstrates core SQL operations:
- Filtering rows using WHERE clauses with dynamic conditions
- Sorting query results using ORDER BY (ASC/DESC)
- Limiting and paging results using LIMIT and OFFSET
"""

import sqlite3
from typing import Any, Dict, List, Optional


class ProductRepository:
    """Manages product catalog data in an SQLite database connection."""

    def __init__(self, db_path: str = ":memory:") -> None:
        """Initialize database connection and ensure schema exists."""
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        """Create the products table if it does not exist."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    def seed_products(self, products: List[Dict[str, Any]]) -> None:
        """Seed initial product records into the database."""
        cursor = self.conn.cursor()
        cursor.executemany(
            """
            INSERT INTO products (name, category, price, stock)
            VALUES (:name, :category, :price, :stock)
            """,
            products,
        )
        self.conn.commit()

    def filter_products(
        self,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_stock: Optional[int] = None,
    ) -> List[sqlite3.Row]:
        """Filter products based on category, price range, and minimum stock."""
        query = "SELECT * FROM products WHERE 1=1"
        params: List[Any] = []

        if category is not None:
            query += " AND category = ?"
            params.append(category)
        if min_price is not None:
            query += " AND price >= ?"
            params.append(min_price)
        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)
        if min_stock is not None:
            query += " AND stock >= ?"
            params.append(min_stock)

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def get_sorted_products(
        self, sort_by: str = "price", order: str = "ASC"
    ) -> List[sqlite3.Row]:
        """Fetch products sorted by a valid column in ascending or descending order."""
        allowed_columns = {"id", "name", "category", "price", "stock"}
        if sort_by not in allowed_columns:
            raise ValueError(f"Invalid sort column: {sort_by}")

        order_upper = order.upper()
        if order_upper not in ("ASC", "DESC"):
            raise ValueError(f"Invalid sort order: {order}")

        query = f"SELECT * FROM products ORDER BY {sort_by} {order_upper}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def get_paginated_products(
        self, 
        limit: int,
        offset: int = 0,
        category: Optional[str] = None,
        sort_by: str = "id",
        order: str = "ASC",
    ) -> List[sqlite3.Row]:
        """Retrieve paginated results with optional filtering and sorting."""
        allowed_columns = {"id", "name", "category", "price", "stock"}
        if sort_by not in allowed_columns:
            raise ValueError(f"Invalid sort column: {sort_by}")

        order_upper = order.upper()
        if order_upper not in ("ASC", "DESC"):
            raise ValueError(f"Invalid sort order: {order}")

        query = "SELECT * FROM products"
        params: List[Any] = []

        if category is not None:
            query += " WHERE category = ?"
            params.append(category)

        query += f" ORDER BY {sort_by} {order_upper} LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()
