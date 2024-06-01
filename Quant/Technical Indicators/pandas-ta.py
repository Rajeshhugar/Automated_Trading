# =============================================================================
# Pandas-TA introduction
# Author : Rajesh Hugar

# Please report bug/issues in the Q&A section
# =============================================================================

from alpha_vantage.timeseries import TimeSeries
import copy
import pandas as pd
import pandas_ta as ta

tickers = ["MSFT", "AAPL", "META", "AMZN", "INTC", "CSCO", "VZ", "IBM", "QCOM", "LYFT"]

# Extract OHLCV data for the tickers
ohlc_tech = {}  # Dictionary with OHLCV values for each stock
key_path = "D:\\OneDrive\\Udemy\\Quantitative Investing Using Python\\1_Getting Data\\AlphaVantage\\key.txt"
ts = TimeSeries(key=open(key_path, 'r').read(), output_format='pandas')

attempt = 0  # Initializing passthrough variable
drop = []  # Initializing list to store tickers whose close price was successfully extracted
while len(tickers) != 0 and attempt <= 5:
    tickers = [j for j in tickers if j not in drop]
    for i in range(len(tickers)):
        try:
            ohlc_tech[tickers[i]] = ts.get_intraday(symbol=tickers[i], interval='30min', outputsize='full')[0]
            ohlc_tech[tickers[i]].columns = ["Open", "High", "Low", "Close", "Volume"]
            drop.append(tickers[i])
        except:
            print(tickers[i], " :failed to fetch data...retrying")
            continue
    attempt += 1

tickers = ohlc_tech.keys()  # Redefine tickers variable after removing any tickers with corrupted data
ohlc_dict = copy.deepcopy(ohlc_tech)  # Create a copy of extracted data

# Apply pandas-ta functions on each dataframe
for ticker in tickers:
    # Calculate momentum indicators (e.g. MACD, ADX, RSI etc.) using pandas-ta
    ohlc_dict[ticker]["ADX"] = ta.adx(ohlc_dict[ticker]["High"],
                                      ohlc_dict[ticker]["Low"],
                                      ohlc_dict[ticker]["Close"],
                                      length=14)['ADX_14']
    # Identify chart patterns (e.g. three white soldiers, engulfing pattern etc.) using pandas-ta
    ohlc_dict[ticker]["3I"] = ta.cdl_pattern(ohlc_dict[ticker], pattern='cdl_3whitesoldiers')

    # Statistical functions (e.g. beta, correlation etc.) using pandas-ta
    ohlc_dict[ticker]["Beta"] = ta.beta(ohlc_dict[ticker]["High"],
                                        ohlc_dict[ticker]["Low"],
                                        length=14)

# Print sample output for a ticker
sample_ticker = list(tickers)[0]
print(ohlc_dict[sample_ticker].tail())
