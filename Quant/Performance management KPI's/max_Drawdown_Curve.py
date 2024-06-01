# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 14:12:09 2024

@author: hugar
"""

import pandas as pd
import matplotlib.pyplot as plt
# Import necesary libraries
import yfinance as yf

# Download historical data for required stocks
tickers = ["AMZN","GOOG","MSFT"]
ohlcv_data = {}

# looping over tickers and storing OHLCV dataframe in dictionary
for ticker in tickers:
    temp = yf.download(ticker,period='6mo',interval='1d')
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = temp

def max_dd(df):
  """
  Calculates the maximum drawdown (MDD) of a trading strategy.

  Args:
      df (pandas.DataFrame): DataFrame containing at least an 'Adj Close' column.

  Returns:
      float: The maximum drawdown as a percentage.

  Raises:
      ValueError: If there is no drawdown in the provided data.
  """

  df = df.copy()
  df["return"] = df["Adj Close"].pct_change()

  # Cumulative return with initial investment accounted for
  df["cum_return"] = (1 + df["return"]).cumprod()

  # Cumulative rolling maximum of cumulative return
  df["cum_roll_max"] = df["cum_return"].cummax()

  # Drawdown (peak return - current return)
  df["drawdown"] = df["cum_roll_max"] - df["cum_return"]

  # Check for no drawdown case (all positive returns)
  if df["drawdown"].max() <= 0:
      raise ValueError("No drawdown found in the data.")

  # MDD as a percentage of peak return
  mdd = (df["drawdown"] / df["cum_roll_max"]).max()

  return mdd * 100,df  # Convert to percentage

# Example usage (assuming your DataFrame is named 'data')
for data in ohlcv_data:
    print(ohlcv_data[data])
    try:
      mdd,df = max_dd(ohlcv_data[data])
      print(df)
      print("Maximum Drawdown:", mdd, "%")
      
      # Plot cumulative return and drawdown
      fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
      ax1.plot(df.index, df["cum_return"], label="Cumulative Return")
      ax2.plot(df.index, df["drawdown"], label="Drawdown")
      ax2.fill_between(df.index, 0, df["drawdown"], color='red', alpha=0.3, label="Drawdown Area")
      ax1.set_ylabel('Cumulative Return')
      ax2.set_ylabel('Drawdown')
      ax2.set_xlabel('Date')
      plt.suptitle('Cumulative Return and Drawdown')
      lines1, labels1 = ax1.get_legend_handles_labels()
      lines2, labels2 = ax2.get_legend_handles_labels()
      plt.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
      plt.tight_layout()
      plt.show()
    
    except ValueError as e:
      print("Error:", e)
  
