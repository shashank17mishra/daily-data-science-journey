"""
Day 18: Date, Time & Timezones
Mastering timezone-aware datetime manipulation, parsing ISO formats,
and scheduling across global timezones using Python's standard library.
"""

from datetime import datetime, time, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class TimezoneManager:
    """Utility class for timezone conversion, business hours checking, and multi-region scheduling."""

    @staticmethod
    def parse_to_utc(dt_str: str) -> datetime:
        """
        Parses an ISO format datetime string into a UTC-aware datetime object.
        If the input is naive, it assumes UTC.
        """
        dt = datetime.fromisoformat(dt_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    @staticmethod
    def convert_timezone(dt: datetime, target_tz_name: str) -> datetime:
        """
        Converts a naive or timezone-aware datetime object to the target timezone.
        If naive, treats the input as UTC.
        """
        try:
            target_tz = ZoneInfo(target_tz_name)
        except ZoneInfoNotFoundError as err:
            raise ValueError(f"Invalid timezone name: {target_tz_name}") from err

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(target_tz)

    @staticmethod
    def is_business_hours(
        dt: datetime,
        tz_name: str,
        start_time: time = time(9, 0),
        end_time: time = time(17, 0),
    ) -> bool:
        """
        Determines whether a given datetime falls within business hours (Monday to Friday,
        start_time to end_time) in a specified target timezone.
        """
        local_dt = TimezoneManager.convert_timezone(dt, tz_name)
        if local_dt.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            return False
        return start_time <= local_dt.time() <= end_time

    @staticmethod
    def generate_tz_schedule(
        utc_dt: datetime, target_timezones: list[str]
    ) -> dict[str, str]:
        """
        Given a UTC datetime and a list of IANA timezone names,
        returns a dictionary mapping each timezone to its ISO-formatted local time string.
        """
        schedule = {}
        if utc_dt.tzinfo is None:
            utc_dt = utc_dt.replace(tzinfo=timezone.utc)

        for tz_name in target_timezones:
            converted = TimezoneManager.convert_timezone(utc_dt, tz_name)
            schedule[tz_name] = converted.isoformat()

        return schedule
