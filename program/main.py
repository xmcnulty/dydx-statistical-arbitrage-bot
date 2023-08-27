import os
import sys

# Get the parent directory of the current script's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

from dydx_connections import connect_dydx
from dydx_private import abort_all_positions, place_market_order
from constants import ABORT_ALL_POSITIONS

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