# -*- coding: utf-8 -*-
"""
MetaTrader5 authentication

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
    
    