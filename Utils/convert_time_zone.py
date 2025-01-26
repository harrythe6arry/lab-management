# utils/timezone_utils.py
from datetime import datetime
import pytz

# Set the Thailand timezone
THAILAND_TZ = pytz.timezone('Asia/Bangkok')

def get_thailand_time():
    """Get the current time in Thailand timezone."""
    return datetime.now(THAILAND_TZ)

def convert_utc_to_thailand_time(utc_time):
    """Convert a UTC datetime object to Thailand timezone."""
    if utc_time.tzinfo is None:
        utc_time = pytz.utc.localize(utc_time)  # Assume naive datetime is UTC
    return utc_time.astimezone(THAILAND_TZ)