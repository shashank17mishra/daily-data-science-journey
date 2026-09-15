"""
Tests for Day 18: Date, Time & Timezones
"""

from datetime import datetime, timezone
import pytest
from learning.python.day_018_date_time_timezones import TimezoneManager


def test_parse_to_utc_naive():
    dt_str = "2023-10-15T14:30:00"
    parsed = TimezoneManager.parse_to_utc(dt_str)
    assert parsed.tzinfo == timezone.utc
    assert parsed.hour == 14


def test_parse_to_utc_aware():
    dt_str = "2023-10-15T14:30:00-04:00"
    parsed = TimezoneManager.parse_to_utc(dt_str)
    assert parsed.tzinfo == timezone.utc
    assert parsed.hour == 18


def test_convert_timezone():
    utc_dt = datetime(2023, 10, 15, 12, 0, tzinfo=timezone.utc)
    ny_dt = TimezoneManager.convert_timezone(utc_dt, "America/New_York")
    assert ny_dt.hour == 8
    assert str(ny_dt.tzinfo) == "America/New_York"


def test_is_business_hours_during_workday():
    # 2023-10-16 is Monday. 14:00 UTC = 10:00 EDT (NY)
    utc_dt = datetime(2023, 10, 16, 14, 0, tzinfo=timezone.utc)
    assert TimezoneManager.is_business_hours(utc_dt, "America/New_York") is True


def test_is_business_hours_after_hours():
    # 2023-10-16 Monday 22:00 UTC = 18:00 EDT (NY)
    utc_dt = datetime(2023, 10, 16, 22, 0, tzinfo=timezone.utc)
    assert TimezoneManager.is_business_hours(utc_dt, "America/New_York") is False


def test_is_business_hours_weekend():
    # 2023-10-14 is Saturday
    utc_dt = datetime(2023, 10, 14, 14, 0, tzinfo=timezone.utc)
    assert TimezoneManager.is_business_hours(utc_dt, "America/New_York") is False


def test_generate_tz_schedule():
    utc_dt = datetime(2023, 10, 15, 12, 0, tzinfo=timezone.utc)
    timezones = ["UTC", "America/New_York", "Asia/Tokyo"]
    schedule = TimezoneManager.generate_tz_schedule(utc_dt, timezones)

    assert "UTC" in schedule
    assert "America/New_York" in schedule
    assert "Asia/Tokyo" in schedule
    assert "2023-10-15T12:00:00+00:00" in schedule["UTC"]
    assert "2023-10-15T21:00:00+09:00" in schedule["Asia/Tokyo"]


def test_invalid_timezone_raises_value_error():
    utc_dt = datetime(2023, 10, 15, 12, 0, tzinfo=timezone.utc)
    with pytest.raises(ValueError, match="Invalid timezone name"):
        TimezoneManager.convert_timezone(utc_dt, "Invalid/Timezone")
