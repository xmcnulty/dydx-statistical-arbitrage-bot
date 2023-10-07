from decouple import config
from dydx3 import Client
from web3 import Web3
from constants import *
from pprint import pprint

# Connect to dydx
def connect_dydx():
    client = Client(
        host=HOST,
        api_key_credentials={
            "key": DYDX_API_KEY,
            "secret": DYDX_API_SECRET,
            "passphrase": DYDX_API_PASSPHRASE
        },
        stark_private_key=STARK_PRIVATE_KEY,
        eth_private_key=ETH_PRIVATE_KEY,
        default_ethereum_address=ETH_ADDRESS,
        web3=Web3(Web3.HTTPProvider(HTTP_PROVIDER))
    ) 

    account = client.private.get_account()
    account_id = account.data["account"]["id"]
    quote_balance = account.data["account"]["quoteBalance"]

    print("Connection successful")
    print("Account id: ", account_id)
    print("Balance: ", quote_balance)

    # Get and print open positions
    open_positions = client.private.get_positions(status="OPEN").data["positions"]

    if len(open_positions) == 0:
        print("No open positions")
    else:
        print("Open positions:")
        
        for position in open_positions:
            print(f" # {position['market']} | {position['side']} | {position['size']}")

        print("-------------------")

    # Get and print orders
    active_orders = client.private.get_orders().data['orders']

    if len(active_orders) == 0:
        print("No active orders")
    else:
        print("Orders:")

        for order in active_orders:
            print(f" # {order['market']} | {order['side']} | {order['size']} | {order['status']}")

        print("-------------------")

    return client