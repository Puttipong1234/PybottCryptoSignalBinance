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

        if i["free"] != "0.00000000" and i["asset"] != "USDT":

            pair_name= i["asset"] + 'BTC'
            print(pair_name)
            
            try:
                trades_buy = client.get_my_trades(symbol=pair_name)
                trades = client.get_historical_trades(symbol=pair_name)
                btc_dif = float(trades[0]["price"]) - float(trades_buy[0]["price"])
                btc_price = float(client.get_historical_trades(symbol='BTCUSDT')[0]["price"])
                percent = (btc_dif/float(trades_buy[0]["price"]))*100

                stat = "ขาดทุน"
                if btc_dif * btc_price > 0:
                    stat = "กำไร"

                this_res = {
                    "name":i["asset"],
                    "val":i["free"],
                    "result": btc_dif * btc_price,
                    "Status": stat,
                    "Percentage": percent
                }

                result.append(this_res)

            except:
                pass


    result.append(this_res)

    print(result)

    return result


if __name__ == "__main__":
    get_holding_performance()
    # trades_buy = client.get_my_trades(symbol="ICXBTC")
    # print(trades_buy)
