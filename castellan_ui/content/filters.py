from datetime import datetime
from horizon.utils import filters as horizon_filters


def timestamp_to_iso(timestamp):
    date = datetime.utcfromtimestamp(timestamp)
    return horizon_filters.parse_isotime(date.isoformat())
