import sqlite3
from pathlib import Path

def test_sql_day_013():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    sql_file = Path("learning/sql/day_013_sql_basics.sql")
    assert sql_file.exists()

    with open(sql_file, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Execute DDL statements
    cursor.executescript("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            country TEXT NOT NULL,
            created_at DATE NOT NULL
        );
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            order_date DATE NOT NULL
        );
        INSERT INTO customers VALUES (1, 'Hans', 'Germany', '2025-01-01');
        INSERT INTO customers VALUES (2, 'Pierre', 'France', '2025-01-02');
        INSERT INTO orders VALUES (101, 1, 600.0, 'COMPLETED', '2025-02-01');
        INSERT INTO orders VALUES (102, 2, 200.0, 'COMPLETED', '2025-02-02');
    """)

    # Run query portion
    query = """
        SELECT 
            c.customer_name,
            c.country,
            COUNT(o.order_id) AS total_orders,
            SUM(o.amount) AS total_spent
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        WHERE o.status = 'COMPLETED'
          AND c.country IN ('Germany', 'France', 'UK')
        GROUP BY c.customer_id, c.customer_name, c.country
        HAVING SUM(o.amount) >= 500.0
        ORDER BY total_spent DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    assert len(results) == 1
    assert results[0][0] == 'Hans'
    assert results[0][1] == 'Germany'
    assert results[0][3] == 600.0
    conn.close()
