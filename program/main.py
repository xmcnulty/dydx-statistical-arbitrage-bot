from pprint import pprint
from dydx_connections import connect_dydx
from dydx_public import construct_market_prices
from dydx_private import abort_all_positions, place_market_order
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS
from cointegration import store_cointigration_results
from pairs_entry import open_positions
from pairs_exit import manage_trade_exits

if __name__ == '__main__':
    
    # Connect to dydx
    try:
        print("Connecting to dydx...")
        client = connect_dydx()
    except Exception as e:
        print("Error connecting to dydx", e)
        exit(1)

    # Abort all positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Aborting all positions...")
            closed_positions = abort_all_positions(client)
        except Exception as e:
            print("Error aborting all positions", e)
            exit(1)

    # Find cointegrated pairs
    if FIND_COINTEGRATED:

        # Construct market prices
        try:
            print("Fetching market prices...")
            df_market_prices = construct_market_prices(client)
        except Exception as e:
            print("Error constructing market prices", e)
            exit(1)

        # Find cointegrated pairs
        try:
            print("Storing cointegrated pairs...")
            stores_result = store_cointigration_results(df_market_prices)

            if stores_result != "saved":
                print("Error storing cointegrated pairs")
                exit(1)
        except Exception as e:
            print("Error storing cointegrated pairs:", e)
            exit(1)

    # Manage exits
    if MANAGE_EXITS:
        try:
            print("Managing exits...")
            manage_trade_exits(client)
        except Exception as e:
            print("Error managing exits", e)
            exit(1)

    # Find and place trades
    if PLACE_TRADES:
        try:
            print("Finding trade opportunities...")
            open_positions(client)
        except Exception as e:
            print("Error finding trade opportunities", e)
            exit(1)