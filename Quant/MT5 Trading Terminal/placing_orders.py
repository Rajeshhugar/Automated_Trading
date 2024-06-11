# -*- coding: utf-8 -*-
"""
MetaTrader5 - placing various order types

@author: Mayank
"""

import MetaTrader5 as mt5
import os

os.chdir(r"C:\DS Learning\Algorithmic Trading\Automated_Trading\Quant\MT5 Trading Terminal") #path where login credentials and server details
key = open("keys.txt","r").read().split()
path = r"C:\Program Files\MetaTrader 5\terminal64.exe"


# establish MetaTrader 5 connection to a specified trading account
if mt5.initialize(path=path,login=int(key[0]), password=key[1], server=key[2]):
    print("connection established")

def place_market_order(symbol,vol,buy_sell,sl_pip,tp_pip):
    pip_unit = 10*mt5.symbol_info(symbol).point
    if buy_sell.capitalize()[0] == "B":
        direction = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
        sl = price - sl_pip*pip_unit
        tp = price + tp_pip*pip_unit
    else:
        direction = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
        sl = price + sl_pip*pip_unit
        tp = price - tp_pip*pip_unit
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": vol,
        "type": direction,
        "price": price,
        "sl": sl,
        "tp":tp,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    
    result = mt5.order_send(request)
    return result

def place_limit_order(symbol,vol,buy_sell,pips_away):
    
    pip_unit = 10*mt5.symbol_info(symbol).point
    
    if buy_sell.capitalize()[0] == "B":
        direction = mt5.ORDER_TYPE_BUY_LIMIT
        price = mt5.symbol_info_tick(symbol).ask - pips_away*pip_unit
    else:
        direction = mt5.ORDER_TYPE_SELL_LIMIT
        price = mt5.symbol_info_tick(symbol).bid + pips_away*pip_unit
        
    
    
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": vol,
        "type": direction,
        "price": price,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    
    result = mt5.order_send(request)
    return result
    
    
place_market_order("USDJPY",0.05,"BUY",5,15)
place_limit_order("GBPUSD",0.02,"Buy",8)
