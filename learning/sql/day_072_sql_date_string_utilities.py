"""
SQL Date & String Utilities Implementation using SQLite.

This module demonstrates intermediate SQL capabilities for string manipulation
(formatting, substring extraction, normalization) and date handling
(parsing, formatting, date arithmetic, tenure calculation).
"""

import sqlite3
from typing import List, Dict, Any


def create_and_populate_db(db_path: str = ":memory:") -> sqlite3.Connection:
    """Creates SQLite tables and populates them with raw sample user and event data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            raw_name TEXT NOT NULL,
            email TEXT NOT NULL,
            registered_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE audit_logs (
            log_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            action_code TEXT NOT NULL,
            logged_at TEXT NOT NULL
        )
    """)

    users_data = [
        (1, "  john DOE ", "John.Doe@EXAMPLE.COM", "2023-01-15 08:30:00"),
        (2, "jane  SMITH", "jane_smith@TechCorp.org", "2023-03-22 14:15:10"),
        (3, "ALICE   wong ", "alice.wong@example.com", "2023-07-01 19:45:00"),
        (4, "bob  MARLEY", "bob@music-hub.io", "2023-11-11 11:11:11"),
        (5, "  charlie BROWN", "charlie.b@techcorp.org", "2024-02-01 09:00:00"),
    ]

    cursor.executemany(
        "INSERT INTO users VALUES (?, ?, ?, ?)",
        users_data
    )

    logs_data = [
        (101, 1, "LOGIN_SUCCESS", "2023-01-15 08:35:00"),
        (102, 1, "PROFILE_UPDATE", "2023-01-16 10:00:00"),
        (103, 2, "LOGIN_SUCCESS", "2023-03-22 14:20:00"),
        (104, 3, "LOGIN_SUCCESS", "2023-07-01 20:00:00"),
        (105, 1, "LOGOUT", "2023-07-02 12:00:00"),
        (106, 5, "LOGIN_SUCCESS", "2024-02-01 09:05:00"),
    ]

    cursor.executemany(
        "INSERT INTO audit_logs VALUES (?, ?, ?, ?)",
        logs_data
    )

    conn.commit()
    return conn


def extract_user_domains(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Extracts email domains using SQL string functions, converts to lowercase,
    and returns domain registration statistics.
    """
    query = """
        SELECT
            LOWER(SUBSTR(email, INSTR(email, '@') + 1)) AS domain,
            COUNT(*) AS user_count
        FROM users
        GROUP BY domain
        ORDER BY user_count DESC, domain ASC
    """
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return [{"domain": row[0], "user_count": row[1]} for row in rows]


def standardize_user_profiles(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Standardizes user full names and formats user IDs.

    Extracts first and last names, handles whitespace, standardizes casing to 'LASTNAME, Firstname',
    and formats user ID into 'USR-000X' format.
    """
    query = """
        WITH cleaned_names AS (
            SELECT
                user_id,
                TRIM(raw_name) AS trimmed_name,
                INSTR(TRIM(raw_name), ' ') AS space_pos
            FROM users
        ),
        split_names AS (
            SELECT
                user_id,
                CASE
                    WHEN space_pos > 0 THEN SUBSTR(trimmed_name, 1, space_pos - 1)
                    ELSE trimmed_name
                END AS first_name,
                CASE
                    WHEN space_pos > 0 THEN TRIM(SUBSTR(trimmed_name, space_pos + 1))
                    ELSE ''
                END AS last_name
            FROM cleaned_names
        )
        SELECT
            user_id,
            PRINTF('USR-%04d', user_id) AS formatted_id,
            UPPER(last_name) || ', ' || UPPER(SUBSTR(first_name, 1, 1)) || LOWER(SUBSTR(first_name, 2)) AS display_name
        FROM split_names
        ORDER BY user_id ASC
    """
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return [
        {
            "user_id": row[0],
            "formatted_id": row[1],
            "display_name": row[2]
        }
        for row in rows
    ]


def calculate_user_tenure(conn: sqlite3.Connection, reference_date: str) -> List[Dict[str, Any]]:
    """Calculates tenure in days relative to reference_date ('YYYY-MM-DD')
    and categorizes users into tenure tiers.
    """
    query = """
        SELECT
            user_id,
            STRFTIME('%Y-%m-%d', registered_at) AS reg_date,
            CAST(JULIANDAY(?) - JULIANDAY(registered_at) AS INTEGER) AS tenure_days,
            CASE
                WHEN (JULIANDAY(?) - JULIANDAY(registered_at)) >= 300 THEN 'Veteran'
                WHEN (JULIANDAY(?) - JULIANDAY(registered_at)) >= 180 THEN 'Established'
                ELSE 'New'
            END AS tenure_tier
        FROM users
        ORDER BY tenure_days DESC
    """
    cursor = conn.cursor()
    cursor.execute(query, (reference_date, reference_date, reference_date))
    rows = cursor.fetchall()
    return [
        {
            "user_id": row[0],
            "reg_date": row[1],
            "tenure_days": row[2],
            "tenure_tier": row[3]
        }
        for row in rows
    ]


def aggregate_monthly_registrations(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Groups user registrations by year-month string and counts total registrations per period."""
    query = """
        SELECT
            STRFTIME('%Y-%m', registered_at) AS year_month,
            COUNT(*) AS registration_count
        FROM users
        GROUP BY year_month
        ORDER BY year_month ASC
    """
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return [{"year_month": row[0], "registration_count": row[1]} for row in rows]
