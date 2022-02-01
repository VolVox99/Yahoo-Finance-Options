from datetime import datetime, timedelta
import pandas_market_calendars as mcal #type: ignore
from time import sleep
from pytz import timezone


nyse = mcal.get_calendar('NYSE')
def market_open():
    tz = 'UTC'
    now = datetime.now(timezone(tz))
    tom = datetime.now(timezone(tz)) + timedelta(days = 10)

    d_range = nyse.schedule(start_date = now, end_date = tom, tz = tz)

    op = nyse.open_at_time(d_range, now)
    return op

