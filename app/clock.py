"""UTC clock for S-6 timestamps (D5, D24); replace `now` in tests."""

from datetime import datetime, timezone


def now() -> datetime:
    return datetime.now(timezone.utc)
