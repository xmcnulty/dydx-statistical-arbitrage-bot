from datetime import datetime, timedelta

# Get timedelta of 100 units for the given interval. Valid intervals are minute, hour, day
def get_timedelta(interval):
    if interval == "minute":
        return timedelta(minutes=100)
    elif interval == "hour":
        return timedelta(hours=100)
    elif interval == "day":
        return timedelta(days=100)
    else:
        raise Exception("Invalid interval")
    
# Format time to ISO string
def formate_time(timestamp):
    return timestamp.replace(microsecond=0).isoformat()

"""
    Returns a dicitonary of time ranges in ISO format. Used for calls to dydx api. API only allows
    100 candles per request, so we need to make multiple requests to get the data we need.

    interval: minute, hour, day
    candles: number of candles to get in multiples of 100
"""
def get_iso_timeranges(interval, candles=400):
    # timedelta of interval=100
    delta = get_timedelta(interval)

    # calculate number of intervals
    intervals = candles / 100

    range_dict = {}

    date_start = datetime.now()

    for i in range(int(intervals)):
        range_dict[f"range_{i}"] = {
            "start": formate_time(date_start - delta),
            "end": formate_time(date_start)
        }

        date_start = date_start - delta

    return range_dict


# Get ISO times
def get_iso_time():

    # get timestamps, for using hourly data
    # api allows maximum of 100 candles per request
    date_start_0 = datetime.now()
    date_start_1 = date_start_0 - timedelta(hours=100)
    date_start_2 = date_start_1 - timedelta(hours=100)
    date_start_3 = date_start_2 - timedelta(hours=100)
    date_start_4 = date_start_3 - timedelta(hours=100)