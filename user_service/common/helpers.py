#common/helper.py

from datetime import datetime, timedelta, timezone
from typing import Union, Optional, Any, Dict, List


def exclude_keys(data: Dict[str, Any], keys_to_exclude: List[str]) -> Dict[str, Any]:
    """
    Returns a copy of the dictionary without the specified keys.
    """
    return {k: v for k, v in data.items() if k not in keys_to_exclude}


def is_truthy(value: Any) -> bool:
    """
    Checks if a value represents a truthy value (like 'yes', '1', 'true').
    """
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def to_camel_case(snake_str: str) -> str:
    """
    Converts a snake_case string to camelCase.
    """
    parts = snake_str.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


def to_snake_case(camel_str: str) -> str:
    """
    Converts a camelCase or PascalCase string to snake_case.
    """
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()


def merge_dicts(base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Shallow-merge two dictionaries, with `updates` overwriting values in `base`.
    """
    return {**base, **updates}


def get_nested(data: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    """
    Safely retrieves a nested value from a dict using a list of keys.
    """
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_utc(dt: Union[str, datetime]) -> datetime:
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.astimezone(timezone.utc)


def convert_timezone(dt: Union[str, datetime], tz: str) -> datetime:
    """
    Convert a datetime object or ISO string to a specific timezone.
    Example: 'Asia/Kolkata', 'America/New_York'
    """
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.astimezone(ZoneInfo(tz))


def get_timezone_now(tz: str) -> datetime:
    """
    Returns the current time in a specific timezone.
    """
    return datetime.now(ZoneInfo(tz))


def get_offset_from_utc(tz: str) -> str:
    """
    Returns the UTC offset of the given timezone.
    """
    now = datetime.now(ZoneInfo(tz))
    offset = now.utcoffset()
    return f"UTC{'+' if offset >= timedelta(0) else '-'}{abs(offset)}"


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    return dt.strftime(fmt)


def parse_datetime(dt_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    return datetime.strptime(dt_str, fmt)


def time_diff_in_seconds(start: datetime, end: Optional[datetime] = None) -> float:
    end = end or get_utc_now()
    return (end - start).total_seconds()


def add_minutes_to_now(minutes: int, tz: str = "UTC") -> datetime:
    return get_timezone_now(tz) + timedelta(minutes=minutes)


def add_days_to_now(days: int, tz: str = "UTC") -> datetime:
    return get_timezone_now(tz) + timedelta(days=days)