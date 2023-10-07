# imports from project files
from constants import CLOSE_AT_ZSCORE_CROSS
from format_utils import format_price
from dydx_private import place_market_order
from dydx_public import get_candles_recent
from cointegration import calculate_z_score

# imports from packages
import time
import json
from pprint import pprint
from pathlib import Path

# imports from dydx
from dydx3.constants import ORDER_SIDE_SELL, ORDER_SIDE_BUY

def manage_trade_exits(client):

    """
    Managing exits based on criteria set in constants.
    """

    save_output = []

    # open active trade json file
    try:
        file_open_positions = open(Path('bot_agents.json'))
        open_positions = json.load(file_open_positions)
    except Exception as e:
        print("Error opening bot_agents.json", e)
        return "complete"
    
    if len(open_positions) < 1:
        return "complete"
    
    # get all open positions
    dydx_open_positions = client.private.get_positions(status="OPEN").data["positions"]
    markets_live = []

    for p in dydx_open_positions:
        markets_live.append(p["market"])

    print("DYDX Open Positions:")
    pprint(markets_live)

    # Check all saved positions match order records
    # Exit trade according to trade rules
    for position in open_positions:
        
        # initialize close trigger
        close = False

        # extract matching markets
        m1 = position["market_1"]
        position_size_m1 = position["order_m1_size"]
        position_side_m1 = position["order_m1_side"]

        m2 = position["market_2"]
        position_size_m2 = position["order_m2_size"]
        position_side_m1 = position["order_m2_side"]

        time.sleep(0.5)

        # get order info for market 1 per exchange
        order_m1 = client.private.get_order_by_id(position["order_id_m1"]).data["order"]
        order_m1_market = order_m1["market"]
        order_m1_size = order_m1["size"]
        order_m1_side = order_m1["side"]

        # get order info for market 2 per exchange
        order_m2 = client.private.get_order_by_id(position["order_id_m2"]).data["order"]
        order_m2_market = order_m2["market"]
        order_m2_size = order_m2["size"]
        order_m2_side = order_m2["side"]

        # Perform matching checks
        check_m1 = m1 == order_m1_market and position_size_m1 == order_m1_size and position_side_m1 == order_m1_side
        check_m2 = m2 == order_m2_market and position_size_m2 == order_m2_size and position_side_m1 == order_m2_side
        check_live = m1 in markets_live and m2 in markets_live

        if not check_m1 or not check_m2 or not check_live:
            print(f"WARNING: Not all open positions match records for: ")
            print(f" # Market (m1, order) - {m1}, {order_m1_market}")
            print(f" # Size (m1, order) - {position_size_m1}, {order_m1_size}")
            print(f" # Side (m1, order) - {position_side_m1}, {order_m1_side}")
            print(f" # Live? {m1 in markets_live}")
            print(f"-------------------")
            print(f" # Market (m2, order) - {m2}, {order_m2_market}")
            print(f" # Size (m2, order) - {position_size_m2}, {order_m2_size}")
            print(f" # Side (m2, order) - {position_side_m1}, {order_m2_side}")
            print(f" # Live? {m2 in markets_live}")
            print(f"-------------------")
            continue

        # get prices
        series1 = get_candles_recent(client, m1)
        series2 = get_candles_recent(client, m2)

        # get markets for reference of tick size
        markets = client.public.get_markets().data

        # trigger close based on z-score
        if CLOSE_AT_ZSCORE_CROSS:

            print(series1[-1], series2[-1])
            
            # initialize z-score
            hedge_ratio = position["hedge_ratio"]
            z_score_traded = position["z_score"]

            if len(series1) > 0 and len(series1) == len(series2):
                spread = series1 - (hedge_ratio * series2)
                z_score_current = calculate_z_score(spread).values.tolist()[-1]