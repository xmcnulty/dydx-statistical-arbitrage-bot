from constants import ZSCORE_THRESHOLD, USD_PER_TRADE, USD_MIN_COLLATERAL
from format_utils import format_price
from dydx_public import get_candles_recent
from dydx_private import has_open_positions
from bot_agent import BotAgent
import pandas as pd
import json
from pprint import pprint

# Open positions
def open_positions(client):

    '''
    Manage finding triggers for trade entry.
    Store trades for managing exits later.
    '''

    # Load cointegrated pairs
    df = pd.read_csv('cointegrated_pairs.csv')

    print(df.head())