# =============================================================================
# Measuring the volatility of a buy and hold strategy
# Author : Mayank Rasu (http://rasuquant.com/wp/)

# Please report bug/issues in the Q&A section
# =============================================================================

# Import necesary libraries
import yfinance as yf
import numpy as np

# Download historical data for required stocks
tickers = ["AMZN","GOOG","MSFT"]
ohlcv_data = {}

# looping over tickers and storing OHLCV dataframe in dictionary
for ticker in tickers:
    temp = yf.download(ticker,period='6mo',interval='1d')
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = temp

def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    vol = df["daily_ret"].std() * np.sqrt(252)
    return vol

for ticker in ohlcv_data:
    print("")

    print("vol for {} = {}".format(ticker,volatility(ohlcv_data[ticker])))