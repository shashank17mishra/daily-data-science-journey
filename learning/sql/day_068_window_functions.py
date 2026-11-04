import sqlite3
from typing import List, Dict, Any, Optional


def create_sample_database(conn: Optional[sqlite3.Connection] = None) -> sqlite3.Connection:
    """Initializes an in-memory SQLite database with sample sales data."""
    if conn is None:
        conn = sqlite3.connect(":memory:")
    
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE daily_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            sale_date TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)
    
    sample_data = [
        ("North", "2023-01-01", 100.0),
        ("North", "2023-01-02", 150.0),
        ("North", "2023-01-03", 120.0),
        ("North", "2023-01-04", 200.0),
        ("South", "2023-01-01", 80.0),
        ("South", "2023-01-02", 90.0),
        ("South", "2023-01-03", 110.0),
        ("South", "2023-01-04", 95.0),
    ]
    
    cursor.executemany("""
        INSERT INTO daily_sales (region, sale_date, amount)
        VALUES (?, ?, ?)
    """, sample_data)
    
    conn.commit()
    return conn


def calculate_daily_growth(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Calculates day-over-day sales difference using LAG window function."""
    query = """
        SELECT
            region,
            sale_date,
            amount,
            LAG(amount, 1, NULL) OVER (
                PARTITION BY region
                ORDER BY sale_date
            ) AS prev_amount,
            ROUND(
                amount - LAG(amount, 1, amount) OVER (
                    PARTITION BY region
                    ORDER BY sale_date
                ), 2
            ) AS amount_change
        FROM daily_sales
        ORDER BY region, sale_date
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return [dict(row) for row in cursor.fetchall()]


def fetch_next_day_sales(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Fetches next day's sale amount using LEAD window function."""
    query = """
        SELECT
            region,
            sale_date,
            amount,
            LEAD(amount, 1, 0.0) OVER (
                PARTITION BY region
                ORDER BY sale_date
            ) AS next_amount
        FROM daily_sales
        ORDER BY region, sale_date
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return [dict(row) for row in cursor.fetchall()]


def calculate_running_total(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Calculates cumulative sales total per region using SUM OVER window function."""
    query = """
        SELECT
            region,
            sale_date,
            amount,
            SUM(amount) OVER (
                PARTITION BY region
                ORDER BY sale_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS running_total
        FROM daily_sales
        ORDER BY region, sale_date
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return [dict(row) for row in cursor.fetchall()]
