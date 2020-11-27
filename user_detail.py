from binance.client import Client
from key import bnbapiKey,bnbapiSecret
client = Client(bnbapiKey, bnbapiSecret)


def get_all_holding_bnb():
    
    holding = []

    for i in client.get_account()["balances"]:
        if i["free"] != "0.00000000" and i["asset"] != "USDT":
            print(i["asset"] , i["free"])

            for j in client.get_ticker():
                if j["symbol"] == i["asset"] + 'BTC' or j["symbol"] == i["asset"] + 'USDT':
                    holding.append({"name":i["asset"],"val":i["free"],"Change":j["priceChangePercent"],"lastPrice":j["lastPrice"]})
    
    return holding