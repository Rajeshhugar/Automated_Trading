# -*- coding: utf-8 -*-
"""
Angel One - Option chain

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

from smartapi import SmartConnect
import yfinance as yf
import os
import urllib
import json
import numpy as np
import pandas as pd
import datetime as dt
from pyotp import TOTP

key_path = r"D:\OneDrive\Udemy\Angel One API"
os.chdir(key_path)

key_secret = open("key.txt","r").read().split()

obj=SmartConnect(api_key=key_secret[0])
data = obj.generateSession(key_secret[2],key_secret[3],TOTP(key_secret[4]).now())

instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
response = urllib.request.urlopen(instrument_url)
instrument_list = json.loads(response.read())

#function to extract all option contracts for a given ticker        
def option_contracts(ticker, option_type="CE", exchange="NFO"):
    option_contracts = []
    for instrument in instrument_list:
        if instrument["name"]==ticker and instrument["instrumenttype"] in ["OPTSTK","OPTIDX"] and instrument["symbol"][-2:]==option_type:
            option_contracts.append(instrument)
    return pd.DataFrame(option_contracts)
        
df_opt_contracts = option_contracts("BANKNIFTY")

#function to extract the closest expiring option contracts
def option_contracts_closest(ticker, duration = 0, option_type="CE", exchange="NFO"):
    #duration = 0 means the closest expiry, 1 means the next closest and so on
    df_opt_contracts = option_contracts(ticker)
    df_opt_contracts["time_to_expiry"] = (pd.to_datetime(df_opt_contracts["expiry"]) - dt.datetime.now()).dt.days
    min_day_count = np.sort(df_opt_contracts["time_to_expiry"].unique())[duration]
    
    return (df_opt_contracts[df_opt_contracts["time_to_expiry"] == min_day_count]).reset_index(drop=True)

df_opt_contracts = option_contracts_closest("BANKNIFTY",1)

#function to extract closest strike options to the underlying price
hist_data = yf.download("^NSEBANK", period='5d')
underlying_price = hist_data["Adj Close"].iloc[-1]

def option_contracts_atm(ticker, underlying_price, duration = 0, option_type="CE", exchange="NFO"):
    #duration = 0 means the closest expiry, 1 means the next closest and so on
    df_opt_contracts = option_contracts_closest(ticker,duration)
    return df_opt_contracts.iloc[abs(pd.to_numeric(df_opt_contracts["strike"])/100 - underlying_price).argmin()]

atm_contract = option_contracts_atm("BANKNIFTY", underlying_price, 0)

#function to extract n closest options to the underlying price
def option_chain(ticker, underlying_price, duration = 0, num = 5, option_type="CE", exchange="NFO"):
    #duration = 0 means the closest expiry, 1 means the next closest and so on
    #num =5 means return 5 option contracts closest to the market
    df_opt_contracts = option_contracts_closest(ticker,duration)
    df_opt_contracts.sort_values(by=["strike"],inplace=True, ignore_index=True)
    atm_idx = abs(df_opt_contracts["strike"] - underlying_price).argmin()
    up = int(num/2)
    dn = num - up
    return df_opt_contracts.iloc[atm_idx-up:atm_idx+dn]
    
opt_chain = option_chain("BANKNIFTY", underlying_price, 0)

