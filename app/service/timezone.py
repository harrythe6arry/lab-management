from datetime import datetime, timezone, timedelta
import pytz

# Set the Thailand timezone
THAILAND_TZ = pytz.timezone('Asia/Bangkok')

def get_thailand_time():
    """Get the current time in Thailand timezone."""
    return datetime.now(THAILAND_TZ)
#
# def convert_utc_to_thailand_time(utc_time):
#     """Convert a UTC datetime object to Thailand timezone."""
#     if utc_time.tzinfo is None:
#         utc_time = pytz.utc.localize(utc_time)  # Assume naive datetime is UTC
#     return utc_time.astimezone(THAILAND_TZ)
#
#
# from datetime import datetime, timezone, timedelta


def convert_utc_to_thailand_time(utc_time):
    """Convert UTC time to Thailand time."""
    if not isinstance(utc_time, datetime):
        # If the input is a date, convert it to a datetime object
        utc_time = datetime.combine(utc_time, datetime.min.time())

    if utc_time.tzinfo is None:
        utc_time = utc_time.replace(tzinfo=timezone.utc)

    thailand_offset = timedelta(hours=7)
    thailand_time = utc_time.astimezone(timezone(timedelta(hours=7)))
    return thailand_time
