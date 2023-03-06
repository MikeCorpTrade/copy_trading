import MetaTrader5 as mt5
from api.mt5_constants import mt5_COEFF, MAGIC, DEVIATION
from api.oanda_mt5_symbols import oanda_mt5_symbols


def login_mt5():
    try:
        authorized = mt5.initialize()
        print(f"authorized accepted: {authorized}")
    except Exception as error:
        print(f"Failed to initialize MT5: {error}")


def map_order_oanda_to_mt5(trade):
    # Map the Oanda trade order to MT5 format

    mt5_SYMBOL = oanda_mt5_symbols[trade["instrument"]]

    mt5_trade_order = {
        "action": mt5.TRADE_ACTION_DEAL,
        "volume": round(trade["units"] * mt5_COEFF, 2),
        "symbol": mt5_SYMBOL,
        "type": mt5.ORDER_TYPE_BUY if trade["units"] > 0 else mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(mt5_SYMBOL).ask,
        "sl": trade["stopLossOnFill"]["price"],
        "tp": trade["takeProfitOnFill"]["price"],
        "comment": "",
        "magic": MAGIC,
        "deviation": DEVIATION,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    return mt5_trade_order
