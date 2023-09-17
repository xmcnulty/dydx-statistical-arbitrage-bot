# imports from project files
from constants import ZSCORE_THRESHOLD, USD_PER_TRADE, USD_MIN_COLLATERAL
from format_utils import format_price
from dydx_public import get_candles_recent
from dydx_private import has_open_positions
from cointegration import calculate_z_score
from bot_agent import BotAgent

# imports from packages
import pandas as pd
import json
from pprint import pprint

# imports from dydx
from dydx3.constants import ORDER_SIDE_SELL, ORDER_SIDE_BUY

# Open positions
def open_positions(client):

    '''
    Manage finding triggers for trade entry.
    Store trades for managing exits later.
    '''

    # Load cointegrated pairs
    df = pd.read_csv('cointegrated_pairs.csv')

    # Get markets for referencing trade size
    markets = client.public.get_markets().data

    # initialize container for bot agent
    bot_agents = []

    # find z-score triggers
    for index, row in df.iterrows():
        
        # exract variables
        base_market = row['base_market']
        quote_market = row['quote_market']
        hedge_ratio = row['hedge_ratio']
        half_life = row['half_life']

        # get prices
        series_1 = get_candles_recent(client, base_market)
        series_2 = get_candles_recent(client, quote_market)

        # calculate z-score
        if len(series_1) > 0 and len(series_1) == len(series_2):
            spread = series_1 - (hedge_ratio * series_2)

            z_score = calculate_z_score(spread).values.tolist()[-1]
            
            if abs(z_score) >= ZSCORE_THRESHOLD:
                
                # check if there are already open positions for this pair
                has_base_position = has_open_positions(client, base_market)
                has_open_position = has_open_positions(client, quote_market)

                # if there are no open positions, create a bot agent
                if not has_base_position and not has_open_position:
                    # determine trade side
                    base_side = ORDER_SIDE_BUY if z_score < 0 else ORDER_SIDE_SELL
                    quote_side = ORDER_SIDE_SELL if z_score > 0 else ORDER_SIDE_BUY

                    # get acceptable price. format to string.
                    base_price = series_1[-1]
                    quote_price = series_2[-1]
                    accept_base_price = float(base_price) * 1.01 if base_side == "BUY" else float(base_price) * 0.99
                    accept_quote_price = float(quote_price) * 1.01 if quote_side == "BUY" else float(quote_price) * 0.99
                    failsafe_base_price = float(base_price) * 0.05 if base_side == "SELL" else float(base_price) * 1.5
                    base_tick_size = markets["markets"][base_market]["tickSize"]
                    quote_tick_size = markets["markets"][quote_market]["tickSize"]

                    # format prices
                    accept_base_price = format_price(accept_base_price, base_tick_size)
                    accept_quote_price = format_price(accept_quote_price, quote_tick_size)
                    accept_fail_base_price = format_price(failsafe_base_price, base_tick_size)

                    # get size
                    # TODO: make this more dynamic. trade sizing
                    base_quantity = 1 / base_price * USD_PER_TRADE
                    quote_quantity = 1 / quote_price * USD_PER_TRADE
                    base_step_size = markets["markets"][base_market]["stepSize"]
                    quote_step_size = markets["markets"][quote_market]["stepSize"]

                    # format sizes
                    base_quantity = format_price(base_quantity, base_step_size)
                    quote_quantity = format_price(quote_quantity, quote_step_size)

                    # ensure size
                    base_min_order_size = markets["markets"][base_market]["minOrderSize"]
                    quote_min_order_size = markets["markets"][quote_market]["minOrderSize"]
                    check_base = float(base_quantity) > float(base_min_order_size)
                    check_quote = float(quote_quantity) > float(quote_min_order_size)

                    # if checks pass, place trades
                    if check_base and check_quote:
                        account = client.private.get_account()
                        free_collateral = float(account.data['account']['freeCollateral'])
                        print(f"Balance: {free_collateral}\nMinimum: {USD_MIN_COLLATERAL}")

                        # ensure proper collateral
                        if free_collateral < USD_MIN_COLLATERAL:
                            break

                        # create bot agent
                        print(base_market, base_side, base_quantity, accept_base_price)
