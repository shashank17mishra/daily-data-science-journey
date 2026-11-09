import sqlite3
import time
from typing import Any, Dict, List, Tuple


class QueryOptimizer:
    """Demonstrates SQL indexing, query plan analysis, and optimization strategies using SQLite."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def create_schema_and_data(self, num_records: int = 5000) -> None:
        """Creates the sample database schema and populates synthetic orders data."""
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS orders")
        cursor.execute(
            """
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                total_amount REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """
        )

        statuses = ["PENDING", "COMPLETED", "CANCELLED", "REFUNDED"]
        records = []
        for i in range(1, num_records + 1):
            customer_id = (i % 100) + 1
            status = statuses[i % len(statuses)]
            total_amount = round((i * 1.5) % 500 + 10.0, 2)
            created_at = f"2023-{(i % 12) + 1:02d}-{(i % 28) + 1:02d} 10:00:00"
            records.append((customer_id, status, total_amount, created_at))

        cursor.executemany(
            "INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES (?, ?, ?, ?)",
            records,
        )
        self.conn.commit()

    def get_query_plan(self, query: str, params: Tuple[Any, ...] = ()) -> List[str]:
        """Runs EXPLAIN QUERY PLAN on the given query and returns line explanations."""
        cursor = self.conn.cursor()
        plan = cursor.execute(f"EXPLAIN QUERY PLAN {query}", params).fetchall()
        # In SQLite, query plan columns are: (id, parent, notused, detail)
        return [row[3] for row in plan]

    def uses_index(self, query: str, params: Tuple[Any, ...] = ()) -> bool:
        """Checks if a query plan uses an index (SEARCH TABLE ... USING INDEX / COVERING INDEX)."""
        plan_details = self.get_query_plan(query, params)
        return any(
            ("USING INDEX" in detail or "USING COVERING INDEX" in detail)
            for detail in plan_details
        )

    def create_single_index(self, index_name: str, table_name: str, column_name: str) -> None:
        """Creates a single-column index."""
        query = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({column_name})"
        self.conn.execute(query)
        self.conn.commit()

    def create_composite_index(self, index_name: str, table_name: str, columns: List[str]) -> None:
        """Creates a composite multi-column index."""
        cols_str = ", ".join(columns)
        query = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({cols_str})"
        self.conn.execute(query)
        self.conn.commit()

    def execute_and_measure(
        self, query: str, params: Tuple[Any, ...] = (), iterations: int = 5
    ) -> Dict[str, Any]:
        """Executes a query multiple times, measures execution time, and returns results summary."""
        cursor = self.conn.cursor()

        # Warm-up run
        cursor.execute(query, params)
        results = cursor.fetchall()

        start_time = time.perf_counter()
        for _ in range(iterations):
            cursor.execute(query, params)
            cursor.fetchall()
        end_time = time.perf_counter()

        avg_time_ms = ((end_time - start_time) / iterations) * 1000.0

        return {
            "result_count": len(results),
            "results": results,
            "avg_time_ms": avg_time_ms,
            "uses_index": self.uses_index(query, params),
            "query_plan": self.get_query_plan(query, params),
        }
