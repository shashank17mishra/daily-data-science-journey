# Day 018: Date, Time & Timezones

## Overview
Learn to manage timezone-aware datetime objects, ISO parsing, timezone conversions, and multi-region business hours evaluation using Python's standard library modules datetime and zoneinfo.

## Objectives
- Master core concepts of Date, Time & Timezones.
- Write clean, tested Python code.

## Key Concepts
This exercise covers timezone management in Python standard library using `datetime` and `zoneinfo` (introduced in Python 3.9):

1. **Naive vs. Timezone-Aware Datetimes**: Naive datetime objects lack explicit timezone metadata (`tzinfo=None`), which can lead to ambiguity. Converting naive datetimes safely requires explicit assignment of timezone context.
2. **Parsing & Standardizing**: `datetime.fromisoformat()` reads standard ISO 8601 strings. Converting all incoming timestamps to UTC ensures consistency across services.
3. **`zoneinfo.ZoneInfo`**: Python's standard library access to the system IANA timezone database, handling daylight saving time (DST) shifts automatically.
4. **Business Logic Across Timezones**: Checking whether a global event timestamp falls within working hours locally requires translating to the destination timezone before checking `weekday()` and `time()` ranges.
