#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
from datetime import datetime
from horizon.utils import filters as horizon_filters


def timestamp_to_iso(timestamp):
    date = datetime.utcfromtimestamp(timestamp)
    return horizon_filters.parse_isotime(date.isoformat())
