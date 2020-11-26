import pandas as pd
from key import *
import talib as ta
import math

import requests
url = 'https://notify-api.line.me/api/notify'
test_token = "2G99oy9nHY5HWJ7Q7uvTLSbRHkm30PDcq7AMcR6OLQl"
# token = 'Hkf9EI7Ilafe4uinK9Iibud1p8OJVMBz8hOLHTCL0gs'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+test_token}

# boughtprice = 18667 # << ราคาซื้อ
# totalamount = 1 # << จำนวนที่ซื้อ
    
# r = requests.post(url, headers=headers, data = {'message':"สั่งซื้อ BTC ไปที่ราคา {} จำนวน {}".format(boughtprice , totalamount) })

def run_bot_trade(res,name,status,Change,amount,lastPrice):
    prof = 0
    current_status = status
    df = pd.DataFrame(res,columns =['date', 'open', 'high', 'low', 'close', 'volume'])

    for i in range(len(df['date'])):
        df['date'][i] = df['date'].values[i]/1000
        df['date'][i] = pd.Timestamp(df['date'][i], unit='s')


    pre_closes = df.iloc[:-1]
    closes = df.iloc[1:]

    highs = closes['high'].to_numpy()
    lows = closes['low'].to_numpy()
    closes = closes['close'].to_numpy()
    pre_closes = pre_closes['close'].to_numpy()

    p1 = 9
    p2 = 15
    p3 = 24
    p4 = 5
    p5 = 5


    sm = 2*p5/10
    atr = ta.ATR(highs, lows, closes, timeperiod=p4)

    ARTX = sm*atr

    s = ta.EMA(closes,p1)-ARTX
    m = ta.EMA(closes,p2)-ARTX
    lg = ta.EMA(closes,p3)-ARTX

    Sht = 0
    Mid = 0
    Lng = 0

    try :
        if closes[-1] == max(closes[-4:-1]):
            Sht = s
            Mid = m
            Lng = lg

        else:

            Sht = ta.EMA(pre_closes,p1)-ARTX
            Mid = ta.EMA(pre_closes,p2)-ARTX
            Lng = ta.EMA(pre_closes,p3)-ARTX

        buylong = False
        sellshort = False

        # print(Sht[-1] > Mid[-1] and Sht[-2] < Mid[-2] and closes[-1] > Sht[-1])
        # print(( Sht[-2] > Lng[-2] and Sht[-1] < Lng[-1] ) or closes[-1] < Lng[-1])
        # print(( Sht[-2] , Lng[-2] , Sht[-1] , Lng[-1] ))
        # print(closes[-1])
        # print(boughtprice > closes[-1])
        # print(boughtprice < closes[-1])
        
        
        if Sht[-1] > Mid[-1] and Sht[-2] < Mid[-2] and closes[-1] > Sht[-1]:
            buylong = True
            if current_status != "BUY NOW":
                r = requests.post(url, headers=headers, data = {'message':"💰💰{} \n🟩🟩BUY NOW \n 🚼🚼Change : {}% \n 💲💲Close : {} \n ".format(name,Change,closes[-1])})
                print("BUY NOW")
                current_status = "BUY NOW"
                prof = closes[-1]
            
            else:
                pass
                # r = requests.post(url, headers=headers, data = {'message':"\nกำลังอยู่ในขาขึ้น \n Close : {} \n ".format(closes[-1])})
                
            # run nitify

        elif ( Sht[-2] > Lng[-2] and Sht[-1] < Lng[-1] ) or closes[-1] < Lng[-1]:
            sellshort = True
            if current_status != "SELL NOW":
                r = requests.post(url, headers=headers, data = {'message':"\n💰💰{} \n🟥🟥SELL NOW \n 🚼🚼Change : {}% \n 💲💲Close : {} \n ".format(name,Change,closes[-1])})
                print("SELL NOW")
                current_status = "SELL NOW"
                prof = amount - closes[-1]
            else:
                pass
                # r = requests.post(url, headers=headers, data = {'message':"\nกำลังอยู่ในขาลง \n Close : {} \n ".format(closes[-1])})
            # run nitify
        
        else:
            r = requests.post(url, headers=headers, data = {'message':"\n💰💰{} \n🦵🦵NO ACTION NOW ! \n 💲💲Close : {} \n ".format(name,closes[-1])})
        
        return current_status , prof

    except:
        return current_status , 0




# boughtprice = 18667 # << ราคาซื้อ
# totalamount = 1 # << จำนวนที่ซื้อ
    
# r = requests.post(url, headers=headers, data = {'message':"สั่งซื้อ BTC ไปที่ราคา {} จำนวน {}".format(boughtprice , totalamount) })

def run_bot_trade_only_buy(res,name,Change,status,amount,lastPrice):
    prof = 0
    current_status = status
    df = pd.DataFrame(res,columns =['date', 'open', 'high', 'low', 'close', 'volume'])

    for i in range(len(df['date'])):
        df['date'][i] = df['date'].values[i]/1000
        df['date'][i] = pd.Timestamp(df['date'][i], unit='s')


    pre_closes = df.iloc[:-1]
    closes = df.iloc[1:]

    highs = closes['high'].to_numpy()
    lows = closes['low'].to_numpy()
    closes = closes['close'].to_numpy()
    pre_closes = pre_closes['close'].to_numpy()

    p1 = 9
    p2 = 15
    p3 = 24
    p4 = 5
    p5 = 5


    sm = 2*p5/10
    atr = ""
    try:
        atr = ta.ATR(highs, lows, closes, timeperiod=p4)
    except :
        return "FAIL" , 0

    ARTX = sm*atr

    s = ta.EMA(closes,p1)-ARTX
    m = ta.EMA(closes,p2)-ARTX
    lg = ta.EMA(closes,p3)-ARTX

    Sht = 0
    Mid = 0
    Lng = 0

    try :
        if closes[-1] == max(closes[-4:-1]):
            Sht = s
            Mid = m
            Lng = lg

        else:

            Sht = ta.EMA(pre_closes,p1)-ARTX
            Mid = ta.EMA(pre_closes,p2)-ARTX
            Lng = ta.EMA(pre_closes,p3)-ARTX

        buylong = False
        sellshort = False

        print(Sht[-1] > Mid[-1] and Sht[-2] < Mid[-2] and closes[-1] > Sht[-1])
        print(( Sht[-2] > Lng[-2] and Sht[-1] < Lng[-1] ) or closes[-1] < Lng[-1])
        print(( Sht[-2] , Lng[-2] , Sht[-1] , Lng[-1] ))
        print(closes[-1])
        # print(boughtprice > closes[-1])
        # print(boughtprice < closes[-1])
        
        
        if Sht[-1] > Mid[-1] and Sht[-2] < Mid[-2] and closes[-1] > Sht[-1]:
            buylong = True
            if current_status != "BUY NOW":
                r = requests.post(url, headers=headers, data = {'message':"💰💰{} \n🟩🟩BUY NOW \n 🚼🚼Change : {}% \n 💲💲Close : {} \n ".format(name,Change,closes[-1])})
                print("BUY NOW")
                current_status = "BUY NOW"
                prof = closes[-1]
            
            else:
                pass
                # r = requests.post(url, headers=headers, data = {'message':"\nกำลังอยู่ในขาขึ้น \n Close : {} \n ".format(closes[-1])})
                
            # run nitify

        elif ( Sht[-2] > Lng[-2] and Sht[-1] < Lng[-1] ) or closes[-1] < Lng[-1]:
            sellshort = True
            if current_status != "SELL NOW":
                # r = requests.post(url, headers=headers, data = {'message':"{} \nSELL NOW \n 🚼🚼Change : {} Close : {} \n ".format(name,clChange,oses[-1])})
                print("SELL NOW")
                current_status = "SELL NOW"
                prof = amount - closes[-1]
            else:
                pass
                # r = requests.post(url, headers=headers, data = {'message':"\nกำลังอยู่ในขาลง \n Close : {} \n ".format(closes[-1])})
            # run nitify
        
        return current_status , prof

    except:
        return current_status , 0