from constants import RESOLUTION, NUM_CANDLES
from time_utils import get_iso_timeranges
import pandas as pd
import numpy as np
import time
from pprint import pprint


ISO_TIMES = get_iso_timeranges(resolution=RESOLUTION, candles=NUM_CANDLES)

# Get historical candles
def get_historical_candles(client, market):
    close_prices = []

    # Extract historical price for each time frame
    for time_frame in ISO_TIMES.keys():
        tf_obj = ISO_TIMES[time_frame]

        start_iso = tf_obj['start']
        end_iso = tf_obj['end']

        candles = client.public.get_candles(
            market=market,
            resolution=str(RESOLUTION), 
            from_iso=start_iso, 
            to_iso=end_iso, 
            limit=100
        )

        # Protect API
        time.sleep(0.2)

        # Structure data
        for candle in candles.data['candles']:
            close_prices.append({'datetime': candle['startedAt'], market: candle['close']})

        # Format and return data
        close_prices.reverse()

        return close_prices


# Construct market prices
def construct_market_prices(client):

    close_prices = get_historical_candles(client, 'BTC-USD')

    pprint(close_prices)

    pass