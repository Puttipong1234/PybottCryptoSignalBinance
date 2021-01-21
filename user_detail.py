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


def get_holding_performance():

    result = []

    for i in client.get_account()["balances"]:

        pair_name_usdt= i["asset"] + 'USDT'
        chk = 0
        try :
            chk = float(client.get_symbol_ticker(symbol=pair_name_usdt)["price"]) * float(i["free"])
        except:
            chk = 0


        if i["free"] != "0.00000000" and i["asset"] != "USDT" and chk > 8 :

            print(pair_name_usdt)
            try:
                trades_buy = client.get_my_trades(symbol=pair_name_usdt)
                # trades = client.get_historical_trades(symbol=pair_name)
                trades = client.get_symbol_ticker(symbol=pair_name_usdt)
                my_total_dif = 0
                total_qty = 0
                for i in trades_buy:
                    my_total_dif += float(i["price"])*float(i["qty"])
                    total_qty += float(i["qty"])

                prof_dif = total_qty*float(trades["price"]) - my_total_dif
                percent = ((total_qty*float(trades["price"]) - my_total_dif))*100/(total_qty*float(trades["price"])

                stat = "ขาดทุน"
                if prof_dif > 0:
                    stat = "กำไร"

                this_res = {
                    "name":i["asset"],
                    "val":i["free"],
                    "result": prof_dif,
                    "Status": stat,
                    "Percentage": (round(percent, 2))
                }

                result.append(this_res)

            except :
                pass


    result.append(this_res)

    if this_res == []:
        this_res = {
                    "name":0,
                    "val":0,
                    "result": 0,
                    "Status": 0,
                    "Percentage": 0
                }


    return result




if __name__ == "__main__":
    # get_holding_performance()
    # trades_buy = client.get_my_trades(symbol="ICXBTC")
    # print(trades_buy)
    # get_holding_performance()

