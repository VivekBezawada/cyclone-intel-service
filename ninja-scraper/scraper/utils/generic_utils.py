from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d %H:%M"


def fetch_timestamp_from_date(date, hours=0):
    date = datetime.strptime(date, DATE_FORMAT) + timedelta(hours=hours)
    return date.timestamp()
