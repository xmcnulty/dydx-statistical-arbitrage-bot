import os
import sys
from dydx_connections import connect_dydx
from dydx_public import construct_market_prices
from dydx_private import abort_all_positions, place_market_order
from constants import ABORT_ALL_POSITIONS, FIND_COINTEGRATED

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