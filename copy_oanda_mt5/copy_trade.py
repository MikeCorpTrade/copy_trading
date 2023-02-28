import MetaTrader5 as mt5

# Oanda trade order details
oanda_order = {
        "units": 1000,
        "instrument": "EUR_USD",
        "timeInForce": "FOK",
        "type": "MARKET",
        "positionFill": "DEFAULT",
        "stopLossOnFill": {
            "timeInForce": "GTC",
            "price": 1.10
        },
        "takeProfitOnFill": {
            "price": 1.20
        }
    }


def map_order_oanda_to_mt5(trade):
    # Map the Oanda trade order to MT5 format
    mt5_trade_order = {
        "volume": trade["units"],
        "symbol": trade["instrument"],
        "type": mt5.ORDER_TYPE_BUY if trade["units"] > 0 else mt5.ORDER_TYPE_SELL,
        "price": 0,
        "sl": trade["stopLossOnFill"]["price"],
        "tp": trade["takeProfitOnFill"]["price"],
        "comment": "",
        "magic": 123456,
        "deviation": 200
    }
    return mt5_trade_order


if __name__ == "__main__":
    mt5_order = map_order_oanda_to_mt5(trade=oanda_order)
    print(mt5_order)
