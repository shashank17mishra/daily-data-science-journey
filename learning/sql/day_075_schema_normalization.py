"""SQL Schema Normalization (1NF to 3NF) implementation in Python using SQLite."""

import sqlite3
from typing import Any, Dict, List, Tuple


class SchemaNormalizer:
    """Manages database schema normalization from Unnormalized Form to 1NF, 2NF, and 3NF."""

    def __init__(self, db_path: str = ":memory:") -> None:
        """Initialize SQLite connection and enable foreign keys."""
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.row_factory = sqlite3.Row

    def close(self) -> None:
        """Close SQLite database connection."""
        self.conn.close()

    def create_unnormalized_table(self) -> None:
        """Create initial unnormalized order records table."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS unnormalized_orders (
                order_id INTEGER,
                order_date TEXT,
                customer_id INTEGER,
                customer_name TEXT,
                customer_zip TEXT,
                city TEXT,
                state TEXT,
                items_csv TEXT
            );
            """
        )
        self.conn.commit()

    def seed_unnormalized_data(self, data: List[Tuple[Any, ...]]) -> None:
        """Seed unnormalized orders table with sample data.

        items_csv format: 'item_id:item_name:price:qty;item_id:item_name:price:qty'
        """
        cursor = self.conn.cursor()
        cursor.executemany(
            """
            INSERT INTO unnormalized_orders 
            (order_id, order_date, customer_id, customer_name, customer_zip, city, state, items_csv)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """,
            data,
        )
        self.conn.commit()

    def migrate_to_1nf(self) -> None:
        """Migrate unnormalized table to 1NF.

        1NF Rules:
        - Values in columns are atomic (no CSV or delimited lists in a cell).
        - Each row is uniquely identifiable (primary key defined).
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE orders_1nf (
                order_id INTEGER,
                order_date TEXT,
                customer_id INTEGER,
                customer_name TEXT,
                customer_zip TEXT,
                city TEXT,
                state TEXT,
                item_id INTEGER,
                item_name TEXT,
                item_price REAL,
                quantity INTEGER,
                PRIMARY KEY (order_id, item_id)
            );
            """
        )

        unnormalized_rows = cursor.execute("SELECT * FROM unnormalized_orders;").fetchall()

        for row in unnormalized_rows:
            items_str = row["items_csv"]
            if not items_str:
                continue
            item_entries = items_str.split(";")
            for entry in item_entries:
                if not entry.strip():
                    continue
                item_id_str, item_name, price_str, qty_str = entry.split(":")
                cursor.execute(
                    """
                    INSERT INTO orders_1nf (
                        order_id, order_date, customer_id, customer_name, customer_zip,
                        city, state, item_id, item_name, item_price, quantity
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        row["order_id"],
                        row["order_date"],
                        row["customer_id"],
                        row["customer_name"],
                        row["customer_zip"],
                        row["city"],
                        row["state"],
                        int(item_id_str),
                        item_name,
                        float(price_str),
                        int(qty_str),
                    ),
                )
        self.conn.commit()

    def migrate_to_2nf(self) -> None:
        """Migrate 1NF to 2NF.

        2NF Rules:
        - Must be in 1NF.
        - Remove partial dependencies (non-key columns must depend on FULL primary key).
        In 1NF, primary key is (order_id, item_id). item_name and item_price depend only on item_id.
        """
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE items_2nf (
                item_id INTEGER PRIMARY KEY,
                item_name TEXT NOT NULL,
                item_price REAL NOT NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE order_items_2nf (
                order_id INTEGER,
                item_id INTEGER,
                quantity INTEGER NOT NULL,
                PRIMARY KEY (order_id, item_id),
                FOREIGN KEY (item_id) REFERENCES items_2nf(item_id)
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE orders_2nf (
                order_id INTEGER PRIMARY KEY,
                order_date TEXT NOT NULL,
                customer_id INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                customer_zip TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL
            );
            """
        )

        cursor.execute(
            """
            INSERT INTO items_2nf (item_id, item_name, item_price)
            SELECT DISTINCT item_id, item_name, item_price FROM orders_1nf;
            """
        )

        cursor.execute(
            """
            INSERT INTO orders_2nf (order_id, order_date, customer_id, customer_name, customer_zip, city, state)
            SELECT DISTINCT order_id, order_date, customer_id, customer_name, customer_zip, city, state FROM orders_1nf;
            """
        )

        cursor.execute(
            """
            INSERT INTO order_items_2nf (order_id, item_id, quantity)
            SELECT order_id, item_id, quantity FROM orders_1nf;
            """
        )

        self.conn.commit()

    def migrate_to_3nf(self) -> None:
        """Migrate 2NF to 3NF.

        3NF Rules:
        - Must be in 2NF.
        - Remove transitive dependencies (non-key columns must not depend on non-key columns).
        In orders_2nf, customer_zip -> city, state is a transitive dependency.
        Also customer_id -> customer_name, customer_zip.
        """
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE zip_locations_3nf (
                zip_code TEXT PRIMARY KEY,
                city TEXT NOT NULL,
                state TEXT NOT NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE customers_3nf (
                customer_id INTEGER PRIMARY KEY,
                customer_name TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                FOREIGN KEY (zip_code) REFERENCES zip_locations_3nf(zip_code)
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE orders_3nf (
                order_id INTEGER PRIMARY KEY,
                order_date TEXT NOT NULL,
                customer_id INTEGER NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers_3nf(customer_id)
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE items_3nf (
                item_id INTEGER PRIMARY KEY,
                item_name TEXT NOT NULL,
                item_price REAL NOT NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE order_items_3nf (
                order_id INTEGER,
                item_id INTEGER,
                quantity INTEGER NOT NULL,
                PRIMARY KEY (order_id, item_id),
                FOREIGN KEY (order_id) REFERENCES orders_3nf(order_id),
                FOREIGN KEY (item_id) REFERENCES items_3nf(item_id)
            );
            """
        )

        cursor.execute(
            """
            INSERT INTO zip_locations_3nf (zip_code, city, state)
            SELECT DISTINCT customer_zip, city, state FROM orders_2nf;
            """
        )

        cursor.execute(
            """
            INSERT INTO customers_3nf (customer_id, customer_name, zip_code)
            SELECT DISTINCT customer_id, customer_name, customer_zip FROM orders_2nf;
            """
        )

        cursor.execute(
            """
            INSERT INTO orders_3nf (order_id, order_date, customer_id)
            SELECT DISTINCT order_id, order_date, customer_id FROM orders_2nf;
            """
        )

        cursor.execute(
            """
            INSERT INTO items_3nf (item_id, item_name, item_price)
            SELECT item_id, item_name, item_price FROM items_2nf;
            """
        )

        cursor.execute(
            """
            INSERT INTO order_items_3nf (order_id, item_id, quantity)
            SELECT order_id, item_id, quantity FROM order_items_2nf;
            """
        )

        self.conn.commit()

    def reconstruct_3nf_to_flat(self) -> List[Dict[str, Any]]:
        """Reconstruct flat dataset using JOINs on 3NF tables to test lossless join property."""
        cursor = self.conn.cursor()
        query = """
            SELECT 
                o.order_id,
                o.order_date,
                c.customer_id,
                c.customer_name,
                c.zip_code AS customer_zip,
                z.city,
                z.state,
                i.item_id,
                i.item_name,
                i.item_price,
                oi.quantity
            FROM orders_3nf o
            JOIN customers_3nf c ON o.customer_id = c.customer_id
            JOIN zip_locations_3nf z ON c.zip_code = z.zip_code
            JOIN order_items_3nf oi ON o.order_id = oi.order_id
            JOIN items_3nf i ON oi.item_id = i.item_id
            ORDER BY o.order_id, i.item_id;
        """
        rows = cursor.execute(query).fetchall()
        return [dict(row) for row in rows]

    def execute_sql(self, sql: str) -> List[Dict[str, Any]]:
        """Execute query and return dictionary representation."""
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
