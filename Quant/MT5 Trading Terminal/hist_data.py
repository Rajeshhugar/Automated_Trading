# -*- coding: utf-8 -*-
"""
MetaTrader5 - Historical data extraction

@author: Mayank
"""

import MetaTrader5 as mt5
import os
import datetime as dt
import pandas as pd

os.chdir(r"C:\DS Learning\Algorithmic Trading\Automated_Trading\Quant\MT5 Trading Terminal") #path where login credentials and server details
key = open("keys.txt","r").read().split()
path = r"C:\Program Files\MetaTrader 5\terminal64.exe"

# establish MetaTrader 5 connection to a specified trading account
if mt5.initialize(path=path,login=int(key[0]), password=key[1], server=key[2]):
    print("connection established")
  
#extract historical data
hist_data = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M15, dt.datetime(2023, 10, 1), 200)   
hist_data_df = pd.DataFrame(hist_data) 
hist_data_df.time = pd.to_datetime(hist_data_df.time, unit="s")
hist_data_df.set_index("time", inplace=True)