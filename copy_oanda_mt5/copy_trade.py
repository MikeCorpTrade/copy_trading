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

mt5_coeff = 9.80E-6

oanda_mt5_symbols = {
    "EUR_USD": "EURUSD"
}


def map_order_oanda_to_mt5(trade):
    # Map the Oanda trade order to MT5 format

    mt5_SYMBOL = oanda_mt5_symbols[trade["instrument"]]

    mt5_trade_order = {
        "action": mt5.TRADE_ACTION_DEAL,
        "volume": round(trade["units"]*mt5_coeff, 2),
        "symbol": mt5_SYMBOL,
        "type": mt5.ORDER_TYPE_BUY if trade["units"] > 0 else mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(mt5_SYMBOL).ask,
        "sl": trade["stopLossOnFill"]["price"],
        "tp": trade["takeProfitOnFill"]["price"],
        "comment": "",
        "magic": 123456,
        "deviation": 200,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    return mt5_trade_order


if __name__ == "__main__":
    mt5_order = map_order_oanda_to_mt5(trade=oanda_order)
    print(mt5_order)
