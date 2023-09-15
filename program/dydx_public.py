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

    tradeable_markets = []
    markets = client.public.get_markets()

    # Find tradeable pairs
    for market in markets.data['markets'].keys():
        market_info = markets.data['markets'][market]

        if market_info['status'] == 'ONLINE' and market_info['type'] == 'PERPETUAL':
            tradeable_markets.append(market)

    # Set initial market prices
    close_prices = get_historical_candles(client, tradeable_markets[0])

    df = pd.DataFrame(close_prices)

    df.set_index('datetime', inplace=True)

    # Add other prices. (Can limit in dev to reduce development time)
    for market in tradeable_markets[1:]:
        additional_prices = get_historical_candles(client, market)
        df_add = pd.DataFrame(additional_prices)
        df_add.set_index('datetime', inplace=True)
        df = pd.merge(df, df_add, how='outer', on='datetime', copy=False)
        del df_add

    # Check for NaNs
    nans = df.columns[df.isna().any()].tolist()

    if len(nans) > 0:
        print("Dropping columns:")
        print(nans)
        df.drop(columns=nans, inplace=True)

    return df

def get_candles_recent(client, market):
    close_prices = []

    # Protect API
    time.sleep(0.2)

    # get candles
    candles = client.public.get_candles(market=market, resolution=str(RESOLUTION), limit=100)

    # Structure data
    for candle in candles.data['candles']:
        close_prices.append(candle['close'])

    close_prices.reverse()
    prices_result = np.array(close_prices).astype(np.float)

    return prices_result