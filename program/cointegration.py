import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from constants import MAX_HALF_LIFE, WINDOW

# Calculate half life
def calculate_half_life(spread):
    df_spread = pd.DataFrame(spread, columns=['spread'])
    spread_lag = df_spread.shift(1)
    spread_lag.iloc[0] = spread_lag.iloc[1]

    spread_return = df_spread - spread_lag
    spread_return.iloc[0] = spread_return.iloc[1]

    spread_lag2 = sm.add_constant(spread_lag)
    model = sm.OLS(spread_return, spread_lag2)

    result = model.fit()

    half_life = round(-np.log(2) / result.params[1], 0)

    return half_life

# Calculate z-score
def calculate_z_score(spread):
    spread_series = pd.Series(spread)
    mean = spread_series.rolling(window=WINDOW, center=False).mean()
    std = spread_series.rolling(window=WINDOW, center=False).std()
    x = spread_series.rolling(window=1, center=False).mean()

    z_score = (x - mean) / std

    return z_score

# Calculate cointegration
def calculate_cointegration(series1, series2):
    series1 = np.array(series1).astype(np.float)
    series2 = np.array(series2).astype(np.float)

    coint_flag = 0
    coint_result = coint(series1, series2)
    coint_t, p_value, critical_value = coint_result[0], coint_result[1], coint_result[2][1]

    model = sm.OLS(series1, series2).fit()
    hedge_ratio = model.params[0]
    spread = series1 - (hedge_ratio * series2)
    half_life = calculate_half_life(spread)

    t_check = coint_t < critical_value

    coint_flag = 1 if t_check and p_value < 0.05 else 0

    return coint_flag, hedge_ratio, half_life


# Store cointegration results
def store_cointigration_results(df_market_prices):
    
    # Initialization
    markets = df_market_prices.columns.tolist()
    criteria_met_pairs = []

    # Find cointegrated pairs
    # Start with base pair
    for index, base_market in enumerate(markets[:-1]):
        series_1 = df_market_prices[base_market].values.astype(float).tolist()

        # Get quote pair
        for quote_market in markets[index + 1:]:
            series_2 = df_market_prices[quote_market].values.astype(float).tolist()

            # Calculate cointegration
            coint_flag, hedge_ratio, half_life = calculate_cointegration(series_1, series_2)

            # Log pairs that meet criteria
            if coint_flag == 1 and half_life <= MAX_HALF_LIFE and half_life > 0:
                criteria_met_pairs.append({
                    'base_market': base_market,
                    'quote_market': quote_market,
                    'hedge_ratio': hedge_ratio,
                    'half_life': half_life
                })
    
    # Create and save dataframe
    df_criteria_met_pairs = pd.DataFrame(criteria_met_pairs)
    df_criteria_met_pairs.to_csv('cointegrated_pairs.csv')

    del df_criteria_met_pairs

    # Return result
    print('Cointegration successfully results saved to data/cointegrated_pairs.csv')

    return "saved"