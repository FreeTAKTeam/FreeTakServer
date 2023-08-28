from datetime import datetime
import datetime as dt
from sqlalchemy import DateTime

DTG_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

def get_dtg(datetime: datetime) -> str:
    """
    Returns a DTG string from a datetime object
    """
    return datetime.strftime(DTG_FMT)

def get_unix(datetime: datetime) -> str:
    """
    Returns a unix timestamp from a datetime object
    """
    return str(datetime.timestamp())

def get_current_dtg(delay = 0) -> str:
    """
    Returns a DTG string from the current time

    Args:
        delay (int): The number of seconds to delay the current time by
    """
    return get_dtg(dt.timedelta(seconds=delay) + datetime.utcnow())

def get_current_unix() -> str:
    """
    Returns a unix timestamp from the current time
    """
    return get_unix(datetime.utcnow())

def get_current_datetime() -> datetime:
    """
    Returns a datetime object from the current time
    """
    return datetime.utcnow()

def get_datetime_from_dtg(dtg: str) -> datetime:
    """
    Returns a datetime object from a DTG string
    """
    return datetime.strptime(dtg, DTG_FMT)

def get_datetime_from_unix(unix: str) -> datetime:
    """
    Returns a datetime object from a unix timestamp
    """
    return datetime.fromtimestamp(float(unix))

def get_past_datetime(seconds_ago: int) -> datetime:
    """
    Returns a datetime object from a number of seconds ago
    """
    return datetime.utcnow() - dt.timedelta(seconds=seconds_ago)
