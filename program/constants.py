from dydx3.constants import API_HOST_GOERLI, API_HOST_MAINNET
from decouple import config
from candle_resolution import CandleResolution


# !!! SELECT MODE !!!
MODE = "DEVELOPMENT"

# Close all positions and open orders
ABORT_ALL_POSITIONS = True

# Find cointegrated pairs
FIND_COINTEGRATED = True

# Place trades
PLACE_TRADES = True

# Resolution
RESOLUTION = CandleResolution._1HOUR

# Number of candles to fetch
NUM_CANDLES = 400

# Stats window for z-score
WINDOW = 21

# Thresholds - Opening
MAX_HALF_LIFE = 24
ZSCORE_THRESHOLD =  1.5
USD_PER_TRADE = 50
USD_MIN_COLLATERAL = 1500

# Thresholds - Closing
CLOSE_AT_ZSCORE_CROSS = True

ETH_ADDRESS = "0xC069dE928F281Da8CB050343915088f492D63532"

# KEYS - Dev
# Must be on Goerli on DYDX
STARK_PRIVATE_KEY_TESTNET = config('STARK_PRIVATE_KEY_TESTNET')
DYDX_API_KEY_TESTNET = config('DYDX_API_KEY_TESTNET')
DYDX_API_SECRET_TESTNET = config('DYDX_API_SECRET_TESTNET')
DYDX_API_PASSPHRASE_TESTNET = config('DYDX_API_PASSPHRASE_TESTNET')
ETH_PRIVATE_KEY = config('ETH_PRIVATE_KEY')

# Keys - exports
STARK_PRIVATE_KEY = STARK_PRIVATE_KEY_TESTNET
DYDX_API_KEY = DYDX_API_KEY_TESTNET
DYDX_API_SECRET = DYDX_API_SECRET_TESTNET
DYDX_API_PASSPHRASE = DYDX_API_PASSPHRASE_TESTNET

# Host - exports
HOST = API_HOST_GOERLI

# HTTP Provider
HTTP_PROVIDER_TESTNET = "https://eth-goerli.g.alchemy.com/v2/i_3tWkyBmJPXCiP5TqRQpyq6fqA03q_V"
HTTP_PROVIDER = HTTP_PROVIDER_TESTNET