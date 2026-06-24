"""
Date and time helper utilities.
"""

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return timezone-aware UTC datetime."""
    return datetime.now(tz=timezone.utc)


def format_datetime(dt: datetime | None, fmt: str = "%Y-%m-%d %H:%M:%S UTC") -> str:
    """Format a datetime to string. Returns empty string for None."""
    if dt is None:
        return ""
    return dt.strftime(fmt)


def days_ago(dt: datetime) -> int:
    """Return number of days since the given datetime."""
    now = utcnow()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = now - dt
    return delta.days
