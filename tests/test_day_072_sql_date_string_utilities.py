import pytest
from learning.sql.day_072_sql_date_string_utilities import (
    create_and_populate_db,
    extract_user_domains,
    standardize_user_profiles,
    calculate_user_tenure,
    aggregate_monthly_registrations,
)


@pytest.fixture
def db_conn():
    conn = create_and_populate_db(":memory:")
    yield conn
    conn.close()


def test_extract_user_domains(db_conn):
    domains = extract_user_domains(db_conn)
    assert len(domains) == 3
    domain_map = {item["domain"]: item["user_count"] for item in domains}
    assert domain_map["example.com"] == 2
    assert domain_map["techcorp.org"] == 2
    assert domain_map["music-hub.io"] == 1


def test_standardize_user_profiles(db_conn):
    profiles = standardize_user_profiles(db_conn)
    assert len(profiles) == 5

    user1 = profiles[0]
    assert user1["user_id"] == 1
    assert user1["formatted_id"] == "USR-0001"
    assert user1["display_name"] == "DOE, John"

    user3 = profiles[2]
    assert user3["display_name"] == "WONG, Alice"


def test_calculate_user_tenure(db_conn):
    reference = "2024-03-01"
    tenures = calculate_user_tenure(db_conn, reference)
    assert len(tenures) == 5

    user1 = next(t for t in tenures if t["user_id"] == 1)
    assert user1["tenure_tier"] == "Veteran"
    assert user1["tenure_days"] > 400

    user5 = next(t for t in tenures if t["user_id"] == 5)
    assert user5["tenure_tier"] == "New"
    assert user5["tenure_days"] < 35


def test_aggregate_monthly_registrations(db_conn):
    monthly = aggregate_monthly_registrations(db_conn)
    assert len(monthly) == 5
    months = [m["year_month"] for m in monthly]
    assert months == ["2023-01", "2023-03", "2023-07", "2023-11", "2024-02"]
    for row in monthly:
        assert row["registration_count"] == 1
