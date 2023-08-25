import os
import sys

# Get the parent directory of the current script's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to the Python path
sys.path.append(parent_dir)

from dydx_connections import connect_dydx

if __name__ == '__main__':
    
    # Connect to dydx
    try:
        client = connect_dydx()
    except Exception as e:
        print(e)
        print("Error connecting to dydx")
        exit(1)