# -*- coding: utf-8 -*-
"""
MetaTrader5 - other important api calls

@author: Mayank
"""

import MetaTrader5 as mt5
import pandas as pd
import os

os.chdir(r"C:\DS Learning\Algorithmic Trading\Automated_Trading\Quant\MT5 Trading Terminal") #path where login credentials and server details
key = open("keys.txt","r").read().split()
path = r"C:\Program Files\MetaTrader 5\terminal64.exe"


# establish MetaTrader 5 connection to a specified trading account
if mt5.initialize(path=path,login=int(key[0]), password=key[1], server=key[2]):
    print("connection established")

def get_position_df():
    positions = mt5.positions_get()
    if len(positions) > 0:
        pos_df = pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        pos_df.time = pd.to_datetime(pos_df.time, unit="s")
        pos_df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
    else:
        pos_df = pd.DataFrame()
        
    return pos_df

def get_orders_df():
    orders = mt5.orders_get()
    if len(orders) > 0:
        ord_df = pd.DataFrame(list(orders),columns=orders[0]._asdict().keys())
        ord_df.time_setup = pd.to_datetime(ord_df.time_setup , unit="s")
        #ord_df.drop(['time_update_msc'], axis=1, inplace=True)
    else:
        ord_df = pd.DataFrame()
        
    return ord_df

get_position_df()
print(get_orders_df())