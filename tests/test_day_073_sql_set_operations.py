"""Unit tests for SQL Set Operations implementation."""

import sqlite3
import pytest
from learning.sql.day_073_sql_set_operations import (
    create_schema_and_seed_data,
    get_unique_customer_emails,
    get_all_customer_emails_with_duplicates,
    get_online_only_customer_emails,
    get_common_customer_emails,
)


@pytest.fixture
def db_connection():
    """Fixture providing an in-memory SQLite database populated with test data."""
    conn = sqlite3.connect(":memory:")
    create_schema_and_seed_data(conn)
    yield conn
    conn.close()


def test_get_unique_customer_emails(db_connection):
    result = get_unique_customer_emails(db_connection)
    expected = [
        "alice@example.com",
        "bob@example.com",
        "charlie@example.com",
        "david@example.com",
        "eve@example.com",
        "frank@example.com",
    ]
    assert result == expected
    assert len(result) == 6


def test_get_all_customer_emails_with_duplicates(db_connection):
    result = get_all_customer_emails_with_duplicates(db_connection)
    expected = [
        "alice@example.com",
        "bob@example.com",
        "charlie@example.com",
        "charlie@example.com",
        "david@example.com",
        "david@example.com",
        "eve@example.com",
        "frank@example.com",
    ]
    assert result == expected
    assert len(result) == 8


def test_get_online_only_customer_emails(db_connection):
    result = get_online_only_customer_emails(db_connection)
    expected = ["alice@example.com", "bob@example.com"]
    assert result == expected


def test_get_common_customer_emails(db_connection):
    result = get_common_customer_emails(db_connection)
    expected = ["charlie@example.com", "david@example.com"]
    assert result == expected


def test_set_operations_empty_tables():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE online_customers (email TEXT);")
    cursor.execute("CREATE TABLE store_customers (email TEXT);")
    conn.commit()

    assert get_unique_customer_emails(conn) == []
    assert get_all_customer_emails_with_duplicates(conn) == []
    assert get_online_only_customer_emails(conn) == []
    assert get_common_customer_emails(conn) == []
    conn.close()
