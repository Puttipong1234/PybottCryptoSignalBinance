import ccxt
import pandas as pd
from key import *
import talib as ta
import math
import time
import csv
import schedule


bnb = ccxt.binance({
    'api_key': bnbapiKey, # API Keys
    'secret': bnbapiSecret
    })

from check import run_bot_trade , run_bot_trade_only_buy
from user_detail import get_all_holding_bnb

import requests
url = 'https://notify-api.line.me/api/notify'
test_token = "2G99oy9nHY5HWJ7Q7uvTLSbRHkm30PDcq7AMcR6OLQl"
# token = 'Hkf9EI7Ilafe4uinK9Iibud1p8OJVMBz8hOLHTCL0gs'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+test_token}





def start_screener_all():
    
    r = requests.post(url, headers=headers, data = {'message':"SCREEN ALL 4H"})
    
    lookup = {}
    # load data
    for key,val in bnb.fetch_tickers().items():
        # if i < 0:
        #     break
        if ("USDT" in key) or ("BTC" in key):
            lookup[key] = val
            lookup[key]["Status"] = "NO ACTION"
            lookup[key]["Total"] = 0
            lookup[key]["Change"] = val["info"]["priceChangePercent"]
            lookup[key]["lastPrice"] = val["info"]["lastPrice"]
    
    
    lookup_holding = lookup
    
    signals_lookup = {}
    
    for key,val in lookup_holding.items():
    
        res = bnb.fetch_ohlcv(key,timeframe='1d',limit=20)
        
        # updated_status , profit = run_bot_trade(res=res,name=key,status=val["Status"],amount=val["Total"],Change=val["Change"],lastPrice=val["lastPrice"])
        updated_status , profit = run_bot_trade_only_buy(res=res,name=key,status=val["Status"],amount=val["Total"],Change=val["Change"],lastPrice=val["lastPrice"])
        
        val["Status"] = updated_status
        if updated_status == "BUY NOW" or updated_status == "SELL NOW":
            signals_lookup[key] = val
            val["TV_Link"] = "https://www.tradingview.com/symbols/{}/".format(key.split("/")[0] + key.split("/")[1])
            val["BNB_Link"] = "https://www.binance.com/en/trade/{}".format(key.split("/")[0] +"_"+ key.split("/")[1])
        #https://www.tradingview.com/symbols/BTCUSD/

    
    # r = requests.post(url, headers=headers, data = {'message':"INVEST PROFIT{} \n \n ".format(total_profit)})
    return signals_lookup


def start_screener():
    
    
    r = requests.post(url, headers=headers, data = {'message':"SCREEN ALL 4H YOU HOLDING"})
    
    
    lookup = {}
    all_holding_list = get_all_holding_bnb()
    # load data
    i = 5
    for key,val in bnb.fetch_tickers().items():
        # if i < 0:
        #     break
        if ("USDT" in key) or ("BTC" in key):
            lookup[key] = val
            lookup[key]["Status"] = "NO ACTION"
            lookup[key]["Total"] = 0
    
    
    # for i in lookup:
    #     res = bnb.fetch_ohlcv(i["name"],timeframe=tf,limit=n)
    #     updated_status , profit = run_bot_trade(res=res,name=i["name"],status=i["Status"],amount=1)
    #     i["Status"] = updated_status
    #     i["Total"] = i["Total"] + profit
    # time.sleep(60*15)
    # print("------------------")
    lookup_holding = {}
    
    for key,val in lookup.items():
        
        
        for i in all_holding_list:
            if i["name"] in key.split("/")[0]: # "BTC" compare to "BTC/USDT"
                lookup_holding[key] = {
                    "Status":"NO ACTION",
                    "Total":i["val"],
                    "Change":i["Change"],
                    "lastPrice":i["lastPrice"]
                }
        
    for key,val in lookup_holding.items():
    
        res = bnb.fetch_ohlcv(key,timeframe='4h',limit=20)
        
        updated_status , profit = run_bot_trade(res=res,name=key,status=val["Status"],amount=val["Total"],Change=val["Change"],lastPrice=val["lastPrice"])
        # updated_status , profit = run_bot_trade_only_buy(res=res,name=key,status=val["Status"],amount=val["Total"],Change=val["Change"],lastPrice=val["lastPrice"])
        
        val["Status"] = updated_status
        val["TV_Link"] = "https://www.tradingview.com/symbols/{}/".format(key.split("/")[0] + key.split("/")[1])
        val["BNB_Link"] = "https://www.binance.com/en/trade/{}".format(key.split("/")[0] +"_"+ key.split("/")[1])

    return lookup_holding
    
    # r = requests.post(url, headers=headers, data = {'message':"INVEST PROFIT{} \n \n ".format(total_profit)})


if __name__ == '__main__':
    start_screener()
    start_screener_all()
    # schedule.every(4).hours.do(start_screener)
    
    while True:
        schedule.run_pending()
        do = input("Press 'X' To Finish , or Press Any key To Summary")
        if do == "x":
            schedule.cancel_job(start_screener)
            print("End Screening")
            csv_file = "Result.csv"
            try:
                with open(csv_file, 'w') as csvfile:
                    d = []
                    d.append("name")
                    d = lookup.keys()
                    writer = csv.DictWriter(csvfile,fieldnames=d)
                    writer.writeheader()
                    for k,v in lookup.items():
                        data = {}
                        data = v
                        data["name"] = k
                        writer.writerow(data)
            except IOError:
                print("I/O error")
        
        else :
            # print("Total Profit Make : {} unit".format(total_profit))
            # print("Total Profit Make each : {} unit".format(lookup))
            continue
        
        time.sleep(1)
    
    
