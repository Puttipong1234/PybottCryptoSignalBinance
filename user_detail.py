from binance.client import Client
from key import bnbapiKey,bnbapiSecret
client = Client(bnbapiKey, bnbapiSecret)

def get_all_holding_bnb():
    
    holding = []
    
    for i in client.get_account()["balances"]:
        if i["free"] != "0.00000000" and i["asset"] != "USDT":
            print(i["asset"] , i["free"])
            holding.append({"name":i["asset"],"val":i["free"]})
    
    return holding