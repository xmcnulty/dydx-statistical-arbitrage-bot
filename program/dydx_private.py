from datetime import datetime, timedelta
from format_utils import format_price
import time

# Returns true if client has open positions for market
def has_open_positions(client, market):

    # Protect API
    time.sleep(0.5)

    all_positions = client.private.get_positions(
        market=market,
        status="OPEN"

    )

    return len(all_positions.data["positions"]) > 0

# Check the status of an order
def check_order_status(client, order_id):
    order = client.private.get_order(order_id)
    
    return order.data["status"]

# Place market order
def place_market_order(client, market, side, size, price, reduce_only):
    # Get position ID
    account_response = client.private.get_account()
    position_id = account_response.data["account"]["positionId"]

    # Expiration time
    server_time = client.public.get_time()
    server_time.data

    # expiration is 1 minute past the server time
    expiration = datetime.fromisoformat(server_time.data["iso"].replace("Z","")) + timedelta(seconds=65)

    # Create order
    placed_order = client.private.create_order(
    position_id=position_id, # required for creating the order signature
    market=market,
    side=side,
    order_type="MARKET",
    post_only=False,
    size=size,
    price=price,
    limit_fee='0.015',
    expiration_epoch_seconds=expiration.timestamp(),
    time_in_force="FOK",
    reduce_only=reduce_only
    )

    return placed_order.data

# Abort all open positions
def abort_all_positions(client):
    # Cancel all orders
    client.private.cancel_all_orders()

    # Protect API
    time.sleep(0.5)

    # Get markets for reference of ticksize
    markets = client.public.get_markets().data
    time.sleep(0.5)

    # Get all open positions
    open_positions = client.private.get_positions(status="OPEN").data["positions"]

    # Handle open positions
    closed_positions = []
    if len(open_positions) > 0:

        # Loop through open positions
        for position in open_positions:

            # Determin market
            market = position["market"]

            # Determine side
            side = "SELL" if position["side"] == "LONG" else "BUY"

            # get price
            price = float(position["entryPrice"])
            accept_price = price * 1.7 if side == "BUY" else price * 0.3
            tick_size = markets["markets"][market]["tickSize"]
            accept_price = format_price(accept_price, tick_size)

            # Place order to close
            order = place_market_order(client, market, side, position["sumOpen"], accept_price, True)

            # Append to closed positions
            closed_positions.append(order)

            # Protect API
            time.sleep(0.2)

    return closed_positions


