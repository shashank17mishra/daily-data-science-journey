"""SQL Set Operations module using SQLite.

Demonstrates set operations:
- UNION: Combines result sets and removes duplicates.
- UNION ALL: Combines result sets preserving all duplicates.
- EXCEPT: Performs set difference (A - B).
- INTERSECT: Performs set intersection (A ∩ B).
"""

import sqlite3
from typing import List


def create_schema_and_seed_data(conn: sqlite3.Connection) -> None:
    """Creates tables and seeds test customer datasets for online and store channels."""
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS online_customers;
        DROP TABLE IF EXISTS store_customers;

        CREATE TABLE online_customers (
            customer_id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL
        );

        CREATE TABLE store_customers (
            customer_id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL
        );

        INSERT INTO online_customers (email, full_name) VALUES
            ('alice@example.com', 'Alice Smith'),
            ('bob@example.com', 'Bob Jones'),
            ('charlie@example.com', 'Charlie Brown'),
            ('david@example.com', 'David Miller');

        INSERT INTO store_customers (email, full_name) VALUES
            ('charlie@example.com', 'Charlie Brown'),
            ('david@example.com', 'David Miller'),
            ('eve@example.com', 'Eve Davis'),
            ('frank@example.com', 'Frank Wilson');
    """)
    conn.commit()


def get_unique_customer_emails(conn: sqlite3.Connection) -> List[str]:
    """Returns deduplicated customer emails from both channels using UNION."""
    query = """
        SELECT email FROM online_customers
        UNION
        SELECT email FROM store_customers
        ORDER BY email ASC;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]


def get_all_customer_emails_with_duplicates(conn: sqlite3.Connection) -> List[str]:
    """Returns all customer emails from both channels including duplicates using UNION ALL."""
    query = """
        SELECT email FROM online_customers
        UNION ALL
        SELECT email FROM store_customers
        ORDER BY email ASC;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]


def get_online_only_customer_emails(conn: sqlite3.Connection) -> List[str]:
    """Returns emails of customers present ONLY in online channel using EXCEPT."""
    query = """
        SELECT email FROM online_customers
        EXCEPT
        SELECT email FROM store_customers
        ORDER BY email ASC;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]


def get_common_customer_emails(conn: sqlite3.Connection) -> List[str]:
    """Returns emails of customers present in BOTH channels using INTERSECT."""
    query = """
        SELECT email FROM online_customers
        INTERSECT
        SELECT email FROM store_customers
        ORDER BY email ASC;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]
