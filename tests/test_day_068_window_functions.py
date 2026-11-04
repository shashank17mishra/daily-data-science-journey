import sqlite3
import pytest
from learning.sql.day_068_window_functions import (
    create_sample_database,
    calculate_daily_growth,
    fetch_next_day_sales,
    calculate_running_total,
)


@pytest.fixture
def db_conn():
    conn = create_sample_database()
    yield conn
    conn.close()


def test_calculate_daily_growth(db_conn):
    results = calculate_daily_growth(db_conn)
    assert len(results) == 8
    
    north_day1 = results[0]
    assert north_day1["region"] == "North"
    assert north_day1["sale_date"] == "2023-01-01"
    assert north_day1["amount"] == 100.0
    assert north_day1["prev_amount"] is None
    assert north_day1["amount_change"] == 0.0
    
    north_day2 = results[1]
    assert north_day2["prev_amount"] == 100.0
    assert north_day2["amount_change"] == 50.0


def test_fetch_next_day_sales(db_conn):
    results = fetch_next_day_sales(db_conn)
    assert len(results) == 8
    
    south_day4 = [r for r in results if r["region"] == "South" and r["sale_date"] == "2023-01-04"][0]
    assert south_day4["next_amount"] == 0.0
    
    south_day1 = [r for r in results if r["region"] == "South" and r["sale_date"] == "2023-01-01"][0]
    assert south_day1["next_amount"] == 90.0


def test_calculate_running_total(db_conn):
    results = calculate_running_total(db_conn)
    
    north_results = [r for r in results if r["region"] == "North"]
    running_totals = [r["running_total"] for r in north_results]
    assert running_totals == [100.0, 250.0, 370.0, 570.0]
    
    south_results = [r for r in results if r["region"] == "South"]
    south_running_totals = [r["running_total"] for r in south_results]
    assert south_running_totals == [80.0, 170.0, 280.0, 375.0]
